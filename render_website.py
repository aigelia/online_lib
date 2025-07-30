import json
import math
import os
import urllib.parse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def prepare_books_data(json_file_name):
    """Получает .json с мета-данными о книгах, возвращает список словарей для рендера."""
    with open(json_file_name, "r", encoding="utf-8") as file:
        books = json.load(file)
    for book in books:
        book['txt_url'] = urllib.parse.quote(book['book_path'], safe='/')
        book['genres'] = book['genres'].replace('.', '').split(', ')
    return books


def render_pages(books, path):
    """Рендерит страницы на основе подготовленных данных."""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')

    books_per_page = 10
    count_pages = math.ceil(len(books) / books_per_page)

    pages = list(chunked(books, books_per_page))

    for index, page_books in enumerate(pages):
        content = list(chunked(page_books, 2))
        rendered_page = template.render(
            content=content,
            page_number=index + 1,
            count_pages=count_pages,
        )
        filename = os.path.join(path, f'index{index + 1}.html')
        with open(filename, 'w', encoding="utf8") as file:
            file.write(rendered_page)

        if index == 0:
            index_path = os.path.join(path, 'index.html')
            with open(index_path, 'w', encoding="utf8") as file:
                file.write(rendered_page)


def rebuild():
    path = 'pages'
    os.makedirs(path, exist_ok=True)

    json_file_name = 'meta_data.json'
    books_chunked = prepare_books_data(json_file_name)

    render_pages(books_chunked, path)


if __name__ == '__main__':
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.watch('pages', rebuild)
    server.watch('render_website.py', rebuild)
    server.serve(root='./pages')

