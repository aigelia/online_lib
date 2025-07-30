import json
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
    return list(chunked(books, 2))


def render_pages(books_chunked, path):
    """Рендерит страницы на основе подготовленных данных."""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')

    pages = chunked(books_chunked, 5)

    for index, content in enumerate(pages):
        rendered_page = template.render(
            content=content,
        )
        with open(f'{path}/index{index+1}.html', 'w', encoding="utf8") as file:
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
    server.serve(root='.')

