import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


def render_page(template):
    with open("meta_data.json", "r") as file:
        books_json = file.read()
    books = json.loads(books_json)
    books_chunked = chunked(books, 2)

    rendered_page = template.render(
        books_chunked=books_chunked,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


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