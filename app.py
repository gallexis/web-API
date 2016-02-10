__author__ = 'alexisgallepe'

import os
from bottle import route, run, template, abort
import xmlParser
import requests
import json


publications = []


@route('/publications/<id:int>')
def get_publication(id):

    global publications
    min = 0
    max = len(publications)
    print(max)
    if id < max and id >= min:
        return publications[id]
    else:
        abort(401,"problem with id parameter")


@route('/authors/<name>')
def get_author_infos(name):
    global publications
    nb_publications = 0
    nb_co_authors = 0

    for publication in publications:
        if name in publication["authors"] :
            print(publication)
            nb_publications+=1
            nb_co_authors = len(publication["authors"])
            print(publication["authors"])

    return json.dumps({ "number_publications":nb_publications , "number_co_authors":nb_co_authors })


@route('/authors/<name>/publications')

@route('/authors/<name>/coauthors')

@route('/search/authors/{searchString}')

@route('/search/publications/{searchString}')

@route('/authors/{name_origine}/distance/{name_destination}')





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


def parseFile():
    parser = xmlParser.XmlParser()
    parser.parse("sample.xml",50)
    return parser.publications

if __name__ == '__main__':
    publications = parseFile()

    port = int(os.environ.get('PORT', 1337))
    run(host='0.0.0.0', port=port, debug=True)