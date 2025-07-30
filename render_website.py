import json
import urllib.parse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_page(template):
    with open("meta_data.json", "r", encoding="utf-8") as file:
        books = json.load(file)

    for book in books:
        # Кодируем путь к файлу в URL, но оставляем слэш нетронутым
        book['txt_url'] = urllib.parse.quote(book['book_path'], safe='/')

    books_chunked = chunked(books, 2)

    rendered_page = template.render(
        books_chunked=books_chunked,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print("index.html updated")


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )
    template = env.get_template('template.html')
    render_page(template)


if __name__ == '__main__':
    rebuild()
    server = Server()
    server.watch('*.html', rebuild)
    server.serve(root='.')
