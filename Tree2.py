__author__ = 'alexisgallepe'


class Tree:

    def __init__(self,publications):
        self.graph = {}
        self.publications = publications

    def get_all_authors(self):
        authors_set = set()

        for publication in self.publications:
            for author in publication["authors"]:
                authors_set.add(author)

        return list(authors_set)


    def create_graph(self, authors):

        for author in authors:
            coauthors_set = set()

            for publication in self.publications:
                if author in publication["authors"]:

                    for a in publication["authors"]:
                        coauthors_set.add(a)

            try:
                coauthors_set.remove(author)
            except:
                pass

            self.graph[author] = list(coauthors_set)

    def find_shortest_path(self, start, end, path=[]):
            start = start.lower()
            end = end.lower()

            path = path + [start]

            if start == end:
                return path
            if not start in self.graph:
                return None

            shortest = None
            for node in self.graph[start]:
                if node not in path:
                    newpath = self.find_shortest_path( node, end, path)
                    if newpath:
                        if not shortest or len(newpath) < len(shortest):
                            shortest = newpath
            return shortest