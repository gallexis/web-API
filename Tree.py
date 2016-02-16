__author__ = 'alexisgallepe'

class Author:



    def __init__(self,nameAuthor, exclude_list, depth=0):
        self.nameAuthor = nameAuthor
        self.exclude_list = exclude_list.append(nameAuthor)
        self.depth = depth

        self.coauthors = []
        self.authors = []
        self.exclude_list = []



    def set_all_coauthors(self, publications):

        coauthors = set()

        for publication in publications:
            if self.nameAuthor in publication["authors"]:

                for author_in_pub in publication["authors"]:
                    if author_in_pub not in self.exclude_list:
                        coauthors.add(author_in_pub)

        try:
            coauthors.remove(self.nameAuthor)
        except:
            pass

        self.coauthors = list(coauthors)

    def rec_authors(self,publications):


        self.set_all_coauthors(publications)
        if len(self.coauthors) == 0:
            return

        self.exclude_list += self.coauthors

        print(self.coauthors, ":", self.nameAuthor, ":", self.exclude_list)
        for author in self.coauthors:
            t = Author(author, self.exclude_list, self.depth + 1)
            t.rec_authors(publications)
            self.authors.append(t)


    def search_author_distance(self,name_author):

        search = None

        for author in self.authors:
            if author.nameAuthor == name_author:
                return self.depth

            depth = author.search_author_distance(name_author)
            if depth is not None:
                return depth


        return search


