import json
import math
import os
import urllib.parse

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

BOOKS_PER_ROW = 2
BOOKS_PER_PAGE = 10


def prepare_books_data(json_file_name):
    with open(json_file_name, 'r', encoding='utf-8') as file:
        books = json.load(file)
    for book in books:
        book['txt_url'] = urllib.parse.quote(book['book_path'], safe='/')
        book['genres'] = book['genres'].replace('.', '').split(', ')
    return books


def render_pages(books, pages_dir):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')

    count_pages = math.ceil(len(books) / BOOKS_PER_PAGE)

    pages = list(chunked(books, BOOKS_PER_PAGE))

    os.makedirs(pages_dir, exist_ok=True)

    debug = os.getenv("DEBUG", "False").lower() == 'true'
    base_path = '/' if debug else '/online_lib/'

    for index, page_books in enumerate(pages):
        content = list(chunked(page_books, BOOKS_PER_ROW))

        rendered_page = template.render(
            content=content,
            page_number=index + 1,
            count_pages=count_pages,
            base_path=base_path,
            debug=debug,
        )

        filename = os.path.join(pages_dir, f'index{index + 1}.html')

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(rendered_page)


def rebuild():
    pages_dir = 'pages'
    json_file_name = 'meta_data.json'
    books = prepare_books_data(json_file_name)
    render_pages(books, pages_dir)


def main():
    load_dotenv()
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.watch('render_website.py', rebuild)
    server.serve(root='.', default_filename='pages/index1.html')


if __name__ == '__main__':
    main()
