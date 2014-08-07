#!/usr/bin/env python

import sys
import requests
from bs4 import BeautifulSoup
from jinja2 import Template

WIKI_URL = "http://en.wikipedia.org/wiki/{name}"
THEME_FILE = "themes/default_light.css"
DEBUG = True

Get = lambda url: requests.get(url)


def read_mapped(func=lambda x:x):
    return map(func, raw_input().strip().split(" "))
def read_int():
    return int(raw_input().strip())
def read_str():
    return raw_input().strip()


print """Book-making format:
new <bookname> <num_pages like 2>
<page 1 name from wiki>
<page 2 name from wiki>
.
.
.
[new <bookname> ...]
end (ends the program)
"""


class ArticleObject:
    def __init__(self, heading, content):
        self.heading = heading
        self.content = content


books = {}

while True:
    inp = raw_input().strip()
    if inp=="end": break

    cmd, bookname, pages = inp.split()
    pages = int(pages)

    if cmd=="new":
        books[bookname] = []

        for i in xrange(pages):
            page_name = read_str().replace(" ", '_')
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
            print "Heading: "+heading.text

            content = soup.find("div", id="bodyContent")
            # print "Content: "+content.text[:100]

            data.append(ArticleObject(heading, content))


    temp = Template(open("template.html").read())
    with open("output/{}.html".format(book), "w") as output_file:
        values = {
            "book_name": book,
            "theme_css": open(THEME_FILE).read(),
            "articles": data
        }
        rendered = temp.render(**values)
        output_file.write(rendered.encode("utf-8"))

    if DEBUG:
        import webbrowser
        webbrowser.open("output/{}.html".format(book))
