__author__ = 'alexisgallepe'

import os
from bottle import route, run, request, response, template, abort
import xmlParser
import json
import re
import logging
import Tree

publications = []

#------------------------------
# function used to add filters in the URL (start and/or count)
def filterUrl_start_count(request):
    start = 0
    count = 100
    try:
        start = int(request.query["start"])
    except:
        pass

    try:
        count = int(request.query["count"])
    except:
        pass

    return (start,count)


def sorting(request,list,start=0,count=0):
    list = list[start:(start+count)]

    try:
        order = request.query["order"]
        list = sorted(list, key=lambda k: k[order])
    except:
        try:
            list = sorted(list)
        except:
            pass

    return list

def restrict_fields(request,list_elt):
    newLst = []
    tmpDict = {}

    try:
        fields = request.query["fields"].lower().split(",")

        for elt in list_elt:
            for key in elt.keys():
                if key in fields:
                    tmpDict[key] = elt[key]

            newLst.append(tmpDict)
            tmpDict = {}

    except:
        return list_elt

    return newLst

# Used in search_publication() to verify if keys:values are correct
def verify_parameters(keysValues,publication):
    if keysValues == []:
        return True

    for key,value in keysValues:
        try:
            #Author is a particular case
            if key == "author":
                if not value in publication["authors"]:
                    return False
                else:
                    continue

            if not publication[key] == value:
                return False
        except:
            return False

    return True

def publication_exists(name_publication,publication_title):
    regex = name_publication.replace("%","(.)").replace("*","(.)*").lower()
    title = publication_title.lower()

    if re.match(regex, title) or name_publication==title:
        return True
    else:
        return False

#------------------------------



"""
    Parametre(s): id de publication <int>

    Format de retour: publications <JSON>

    Erreurs possibles: <JSON>
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


"""
    Parametre(s): Nom d'un auteur <string>

    Format de retour: Nombre de publications, nombre co-auteurs <JSON>

    Erreurs possibles: S'il n'y a pas d'auteur, retourne une structure vide <JSON>
"""
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


"""
    Parametre(s): Nom d'un auteur <string>

    Format de retour:  Auteur, Publications <JSON>

    Erreurs possibles: S'il n'y a pas d'auteur ou publication, retourne une structure vide <JSON>
"""
@route('/authors/<author_name>/publications')
def get_author_publications(author_name):
    list_publications = []
    author_name = author_name.lower()

    for publication in publications:
        if author_name in publication["authors"]:
            list_publications.append(publication)

    start,count = filterUrl_start_count(request)
    list_publications = sorting(request,list_publications,start,count)
    list_publications = restrict_fields(request,list_publications)

    return json.dumps({ "author":author_name , "publications": list_publications})


"""
    Parametre(s): Nom d'un auteur <string>

    Format de retour:  Auteur, Co-auteur <JSON>

    Erreur possible: l'auteur n'existe pas <JSON>
"""
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

    start,count = filterUrl_start_count(request)
    list_coauthors = sorting(request,list(list_coauthors),start,count)
    return json.dumps({ "author":author_name , "coauthors": list_coauthors })


"""
    Parametre(s): Nom d'un auteur (regex autorisées) <string>

    Format de retour:  Auteurs <JSON>

    Erreurs possibles: S'il n'y a pas d'auteur ou publication, retourne une structure vide <JSON>
"""
@route('/search/authors/<searchString>')
def search_authors(searchString):
    matchs = set()
    regex = searchString.replace("%","(.)").replace("*","(.)*").lower()

    for publication in publications:
        for author in publication["authors"]:

            if re.match(regex, author.lower()):
                matchs.add( author )

    start,count = filterUrl_start_count(request)
    matchs = sorting(request,list(matchs),start,count)
    return json.dumps( {"authors": matchs } )



"""
    Parametre(s): Titre d'une publication <string>

    Format de retour:  Publications <JSON>

    Erreurs possibles: S'il n'y a pas d'auteur ou publication, retourne une structure vide <JSON>
"""
@route('/search/publications/<name_publication>')
def search_publication(name_publication):

    keysValues = []
    name_publication = name_publication.lower()
    matchs = []

    try:
        parameters = request.query["filter"].lower()

        keysValues = parameters.split(",")
        for i,key_value in enumerate(keysValues):
            key,value = key_value.split(':')
            keysValues[i] = (key,value)
    except:
        pass

    for publication in publications:
        if publication_exists(name_publication,publication["title"]) and verify_parameters(keysValues,publication):
            matchs.append(publication)

    start,count = filterUrl_start_count(request)
    matchs = sorting(request,matchs,start,count)
    matchs = restrict_fields(request,matchs)

    return json.dumps( {"publications": matchs } )


"""
    Parametre(s): Nom d'un auteur <string> & Nom d'un autre auteur <string>

    Format de retour:  Auteur, Auteur, Profondeur <JSON>

    Erreurs possibles: Auteur d'origine ou de destination ou les deux n'existent pas <JSON>
"""
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
    #parser.read_binaryMode("publications_big.bin")
    parser.read_binaryMode("publications.bin")
    return parser.publications

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    publications = parseFile()
    logging.info("Loaded: "+str(len(publications))+" publications.")

    response.content_type = 'application/json'
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
