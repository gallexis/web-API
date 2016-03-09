__author__ = 'alexisgallepe'

import os
from bottle import route, run, request, response, template, abort
import xmlParser
import requests
import json
import re
import Tree
import logging

publications = []

@route('/publications/<id:int>')
def get_publication(id):

    min = 0
    max = len(publications)
    logging.info(max)
    if id < max and id >= min:
        return json.dumps(publications[id])
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


def verify_parameters(keysValues,publication):
    if keysValues == []:
        return True

    for key,value in keysValues:
        try:

            #Autor is a particular case
            if key == "author":
                if not value in publication["authors"]:
                    return False
                else:
                    continue

            if not publication[key] == value:
                return False

        except Exception as e:
            print(e)
            return False

    return True


@route('/search/publications/<url>')
def search_publication(url):
    keysValues = []
    url = url.lower()

    try:
        parameters = request.query["filter"].lower()

        keysValues = parameters.split(",")
        for i,key_value in enumerate(keysValues):
            key,value = key_value.split(':')
            keysValues[i] = (key,value)

    except:
        pass

    for publication in publications:
        if url in publication["title"] and verify_parameters(keysValues,publication):
            return json.dumps(publication)


"""
@route('/authors/<name_origine>/distance/<name_destination>')
@route('/title/<url:path>')
@route('/arbre/<id:int>')
"""



def parseFile():
    parser = xmlParser.XmlParser()
    parser.parse("sample.xml",50)
    return parser.publications

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    publications = parseFile()
    t = Tree.Author("codd",[])
    t.create_tree(publications)
    logging.info(t.get_depth("alexis"))

    port = int(os.environ.get('PORT', 8080))
    response.content_type = 'application/json'
    run(host='0.0.0.0', port=port, debug=True)