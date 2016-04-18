__author__ = 'alexisgallepe'

import os
from bottle import route, run, request, response, template, abort
import xmlParser
import requests
import json
import re
import logging
import Tree

publications = []


# newlist = sorted(list_to_be_sorted, key=lambda k: k['name'])
# https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-values-of-the-dictionary-in-python

"""
    params:

    return format:

    errors possible:
"""
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
    author_name = author_name.lower()

    for publication in publications:
        if author_name in publication["authors"] :
            nb_publications+=1
            nb_co_authors = len(publication["authors"])

    return json.dumps({ "number_publications":nb_publications , "number_co_authors":nb_co_authors })

# ?? return uniquement les titles ??
@route('/authors/<author_name>/publications')
def get_author_publications(author_name):
    list_publications = []
    author_name = author_name.lower()

    for publication in publications:
        if author_name in publication["authors"]:
            list_publications.append(publication["title"])

    return json.dumps({ "author":author_name , "publications":list_publications })


@route('/authors/<author_name>/coauthors')
def get_coauthors(author_name):
    list_coauthors = set()
    author_name = author_name.lower()

    for publication in publications:
        if author_name in publication["authors"]:

            for author in publication["authors"]:
                list_coauthors.add(author)

    try:
        list_coauthors.remove(author_name)
    except:
        return json.dumps({ "error": "author does not exist"})

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

# Used in search_publication() to verify if keys:values are correct
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


@route('/authors/<name_origine>/distance/<name_destination>')
def distance_between_authors(name_origine,name_destination):
    does_name_origine_exists = False
    does_name_destination_exists = False
    name_origine = name_origine.lower()
    name_destination = name_destination.lower()

    # Verify if name_origine and name_destination exist
    for publication in publications:
        if name_origine in publication["authors"]:
            does_name_origine_exists = True

        if name_destination in publication["authors"]:
            does_name_destination_exists = True

    if does_name_origine_exists == False and does_name_destination_exists == False:
        return json.dumps({ "error": "author_origine and author_destination don't exist"})
    elif does_name_origine_exists == False:
        return json.dumps({ "error": "author_origine doesn't exist"})
    elif does_name_destination_exists == False:
        return json.dumps({ "error": "author_destination doesn't exist"})


    tree = Tree.Author(name_origine,[])
    tree.create_tree(publications)
    depth = tree.get_depth(name_destination)


    return json.dumps({"author_origine":name_origine,"author_destination":name_destination,"depth":depth})


def parseFile():
    parser = xmlParser.XmlParser()
    #parser.parse("sample.xml",100)
    parser.read_binaryMode()
    return parser.publications


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    publications = parseFile()[:5000]

    t = Tree.Tree(publications)
    a = t.get_all_authors()
    t.create_graph(a)
    print(len(a))
    print(t.find_shortest_path("Oliver Gronz","Markus Casper" ))


    """
    logging.info("Loaded: "+str(len(publications))+" publications.")
    response.content_type = 'application/json'
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
    """