__author__ = 'alexisgallepe'

import os
from bottle import route, run, template, abort
import xmlParser
import requests
import json
import re
import Tree

publications = []

@route('/publications/<id:int>')
def get_publication(id):

    min = 0
    max = len(publications)
    print(max)
    if id < max and id >= min:
        return publications[id]
    else:
        return json.dumps({ "error": "problem with id parameter" })


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

    matchs = set()
    regex = searchString.replace("%","(.)").replace("*","(.)*").lower()

    for publication in publications:
        for author in publication["authors"]:

            if re.match(regex, author.lower()):
                matchs.add( author )

    return json.dumps( {"authors": list(matchs)} )


"""
@route('/search/publications/<searchString>')

@route('/authors/<name_origine>/distance/<name_destination>')




@route('/title/<url:path>')
@route('/arbre/<id:int>')
"""



def parseFile():
    parser = xmlParser.XmlParser()
    parser.parse("sample.xml",50)
    return parser.publications

if __name__ == '__main__':
    publications = parseFile()
    t = Tree.Author("Codd",[])
    t.rec_authors(publications)
    print(t.search_author_distance("Alexis"))
    #port = int(os.environ.get('PORT', 8080))
    #run(host='0.0.0.0', port=port, debug=True)