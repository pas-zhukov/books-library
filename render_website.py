from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():

    render_page()

    server = Server()

    server.watch('index_template.html', render_page)

    server.serve(root='.')


def render_page():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('index_template.html')

    rendered_page = template.render(
        books=get_books_stats('library_books/books_metadata.json')
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    print('Page rendered!')


def get_books_stats(path_to_json: str):
    with open(path_to_json, 'r', encoding='utf-8') as file:
        books = json.load(file)
    return books


if __name__ == "__main__":
    main()
