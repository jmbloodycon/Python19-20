import re

r = re.compile(r'(/\*\*(.*?\n?)+?\*/(\n.*))')


def find_all_docstrings(fie_name):
    with open(fie_name, encoding='utf-8') as f:
        str_file = f.read()
        all_docstrings = re.findall(r, str_file)
    return all_docstrings


def make_string(all_doc_with_func, file_name):
    text = f'<h1 style="color:blue;">Модуль {file_name[:-5]}</h1>'
    for tuple_string in all_doc_with_func:
        body = tuple_string[0].split('\n')
        head = tuple_string[2].replace('{', '')
        head = head.replace(';', '')
        text += f'<h1 style="color:red;">{head}</h1>'
        for i in body[:-1]:
            i = i.replace('*', '')
            i = i.replace('/', '')
            text += f'<p>{i}</p>'
    return text


def to_page(string):
    return f'<!DOCTYPE html><html><head>' \
        f'<meta charset="utf-8"><title>Javadoc</title></head>' \
        f'<body>{string}</body></html>'


def save_html(name, html):
    with open(name + '.html', 'w', encoding='utf-8') as f:
        f.write(html)


def run():
    res = find_all_docstrings('java_doc.java')
    html = make_string(res, 'java_doc.java')
    page = to_page(html)
    save_html('mod', page)


if __name__ == '__main__':
    run()
