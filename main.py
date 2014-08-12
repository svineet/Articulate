#!/usr/bin/env python

import sys
import requests
from bs4 import BeautifulSoup
from jinja2 import Template

WIKI_URL = "http://en.wikipedia.org/wiki/{name}"
WIKI_CSS = "wikipedia_css.css"
THEME_FILE = "themes/default_light.css"
DEBUG = False

Get = lambda url: requests.get(url)


def read_mapped(func=lambda x:x):
    return map(func, raw_input().strip().split(" "))
def read_int():
    return int(raw_input().strip())
def read_str():
    return raw_input().strip()


class ArticleObject:
    def __init__(self, heading, content):
        self.heading = heading
        self.content = content


books = {}

while True:
    inp = raw_input().strip()
    if inp=="end": break

    inp = inp.split(" ")
    cmd = inp[0]
    bookname = " ".join(inp[1:])

    if cmd=="new":
        books[bookname] = []

        while True:
            page_name = read_str()
            if page_name=="end book":
                break

            page_name = page_name.replace(" ", '_')
            books[bookname].append(page_name)


print "Beginning processing books. This might take some time. Go listen to Coldplay."

for book in books.iterkeys():
    articles = books[book]
    data = []
    for article in articles:
        print "Processing article {}".format(article)
        url = WIKI_URL.format(name=article)
        r = Get(url)
        if r.status_code!=requests.codes.ok:
            print "Error occurred processing article {}"\
                    .format(article)
            print "Status code: {}".format(r.status_code)
        else:
            soup = BeautifulSoup(r.text)

            heading = soup.find("h1", id="firstHeading")
            # print "Heading: "+heading.text

            content = soup.find("div", id="bodyContent")
            # print "Content: "+content.text[:100]

            data.append(ArticleObject(heading, content))


    temp = Template(open("template.html").read())
    with open("output/{}.html".format(book), "w") as output_file:
        values = {
            "book_name": book,
            "wiki_css": open(WIKI_CSS).read(),
            "theme_css": open(THEME_FILE).read(),
            "articles": data
        }
        rendered = temp.render(**values)
        output_file.write(rendered.encode("utf-8"))

    if DEBUG:
        import webbrowser
        webbrowser.open("output/{}.html".format(book))
