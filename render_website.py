import json
import os
from argparse import ArgumentParser
from urllib.parse import urljoin

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

MAX_BOOKS_COUNT = 100
BOOKS_ON_PAGE = 10


def main():
    cmd_args = parse_arguments()
    render_pages()

    if not cmd_args.render_once:
        server = Server()
        server.watch(cmd_args.template, render_pages)
        server.serve(root='.')


def render_pages(template_path: str = 'template.html',
                 pages_catalog: str = 'pages/',
                 library_path: str = 'media/'):
    render_index(pages_catalog)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(template_path)
    books = get_books_stats(os.path.join(library_path, 'books_metadata.json'))[:MAX_BOOKS_COUNT]
    books = tuple(chunked(books, BOOKS_ON_PAGE))
    os.makedirs(pages_catalog, exist_ok=True)
    for index, books_set in enumerate(books, 1):
        books_set = tuple(chunked(books_set, int(len(books_set)/2)))
        rendered_page = template.render(
            books_set=books_set,
            pages_count=len(books),
            page_number=index
        )
        with open(os.path.join(pages_catalog, f'index{index}.html'), 'w+', encoding='utf8') as file:
            file.write(rendered_page)


def render_index(pages_catalog: str = 'pages/'):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('index_template.html')
    rendered_page = template.render(
        pages_catalog=urljoin(pages_catalog, 'index1.html')
    )
    with open('index.html', 'w+', encoding='utf8') as file:
        file.write(rendered_page)


def get_books_stats(path_to_json: str):
    with open(path_to_json, 'r', encoding='utf-8') as file:
        books = json.load(file)
    return books


def parse_arguments():
    parser = ArgumentParser(description='Local site hosting.')
    parser.add_argument(
        '-t',
        '--template',
        default='template.html',
        help='Template html to render.'
    )
    parser.add_argument(
        '--render_once',
        help='Render pages without running a server.',
        action='store_true',
        default=False
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
