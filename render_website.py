from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json


from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked

PAGES_CATALOG = 'pages/'
MAX_BOOKS_COUNT = 200
BOOKS_ON_PAGE = 10


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

    books = get_books_stats('library_books/books_metadata.json')[:MAX_BOOKS_COUNT]
    books = tuple(chunked(books, BOOKS_ON_PAGE))
    os.makedirs(PAGES_CATALOG, exist_ok=True)
    for index, books_set in enumerate(books):
        books_set = tuple(chunked(books_set, int(BOOKS_ON_PAGE/2)))
        rendered_page = template.render(
            books_col_1=books_set[0],
            books_col_2=books_set[1],
            pages_count=len(books),
            page_number=index+1
        )

        with open(os.path.join(PAGES_CATALOG, f'index{index+1}.html'), 'w+', encoding="utf8") as file:
            file.write(rendered_page)

    print('Pages rendered!')


def get_books_stats(path_to_json: str):
    with open(path_to_json, 'r', encoding='utf-8') as file:
        books = json.load(file)
    return books


if __name__ == "__main__":
    main()
