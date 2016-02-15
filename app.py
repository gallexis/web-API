__author__ = 'alexisgallepe'

import os
from bottle import route, run, template, abort
import xmlParser
import requests
import json
import re


publications = []


@route('/publications/<id:int>')
def get_publication(id):

    min = 0
    max = len(publications)
    print(max)
    if id < max and id >= min:
        return publications[id]
    else:
        abort(401,"problem with id parameter")


@route('/authors/<author_name>')
def get_author_infos(author_name):
    nb_publications = 0
    nb_co_authors = 0

    for publication in publications:
        if author_name in publication["authors"] :
            nb_publications+=1
            nb_co_authors = len(publication["authors"])

    return json.dumps({ "number_publications":nb_publications , "number_co_authors":nb_co_authors })

# ?? return uniquement les titles ??
@route('/authors/<author_name>/publications')
def get_author_publications(author_name):

    list_publications = []

    for publication in publications:
        if author_name in publication["authors"]:
            list_publications.append(publication["title"])

    return json.dumps({ "author":author_name , "publications":list_publications })



@route('/authors/<author_name>/coauthors')
def get_coauthors(author_name):

    list_coauthors = set()

    for publication in publications:
        if author_name in publication["authors"]:

            for author in publication["authors"]:
                list_coauthors.add(author)

    list_coauthors.remove(author_name)

    return json.dumps({ "author":author_name , "coauthors": list(list_coauthors) })


@route('/search/authors/<searchString>')
def search_authors(searchString):

    regex = searchString.replace("%","(.)").replace("*","(.)*")
    for publication in publications:
        for author in publication["authors"]:
            print(regex,' : ',author)
            if re.match(regex, author):
                return get_author_infos(author)

    return json.dumps({ "error": "Author not found" })


@route('/search/publications/<searchString>')

@route('/authors/<name_origine>/distance/<name_destination>')







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

    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)