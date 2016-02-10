__author__ = 'alexisgallepe'

import os
from bottle import route, run, template
import xmlParser
import requests
import json


publications = []

@route('/')
def index():
    return "eee"


@route('/search/arbres/<query>')
def search_trees(query):
    trees100 = []
    params = ["hauteur","circonference"]
    param = query.split(":")

    value = param[1]
    param = param[0]

    if param not in params:
        return "error"

    for tree in parsedTrees:
        if tree[param] == value and len(trees100) < 100:
            trees100.append(tree)


    return json.dumps(trees100)


@route('/title/<url:path>')
def title(url):
    r = requests.get(url)

    parser = MyHTMLParser()
    parser.feed(r.text)

    return "Titre: " + parser.title


@route('/arbre/<id:int>')
def get_tree_by_id(id):
    min = 0
    max = len(parsedTrees)
    print(max)

    if id <= max and id >= min:
        return parsedTrees[id]
    else:
        return "error"


@route('/licence')
def content():
    return json.dumps(parsedTrees)

def parseFile():
    parser = xmlParser.XmlParser()
    parser.parse("sample.xml",50)
    return parser.publications

if __name__ == '__main__':
    print("Parsing File")
    publications = parseFile()


    port = int(os.environ.get('PORT', 1337))
    run(host='0.0.0.0', port=port, debug=True)