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


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    render_page(template)
    # server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()
    server = Server()
    server.watch('/*.html', shell('make html', cwd='docs'))
    server.serve(root='.')


if __name__ == '__main__':
    main()