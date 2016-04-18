__author__ = 'alexisgallepe'

import logging

class Author:

    def __init__(self,name_author, exclude_list, depth=1):
        self.name_author = name_author.lower()
        self.depth = depth

        self.exclude_list = exclude_list
        self.exclude_list.append(name_author)

        self.coauthors = []
        self.authors = []

    """
        Put in self.coauthors every co-author of self.nameAuthor
    """
    def set_all_coauthors(self, publications):
        coauthors = set()

        for publication in publications:
            if self.name_author in publication["authors"]:

                for author in publication["authors"]:
                    if author not in self.exclude_list:
                        coauthors.add(author)

        try:
            coauthors.remove(self.name_author)
        except:
            pass

        self.coauthors = list(coauthors)


    """
        Recursive function that creates the tree of authors.
        It creates a class "Author" for every co-author in self.coauthors,
            then call create_tree on this class,
            and add +1 to the depth

        self.exclude_list is here to avoid infinite loops, by excluding authors
        who are already member of the tree
    """
    def create_tree(self,publications):

        self.set_all_coauthors(publications)
        if len(self.coauthors) == 0:
            return

        self.exclude_list += self.coauthors

        # list( set(  .. ) ) is to remove the duplicates authors in the exclude_list
        self.exclude_list = list(set(self.exclude_list))
        print(self.coauthors)

        logging.info("\n -- Current author: " + self.name_author +
                     "\n -- Co-authors: " + ", ".join(self.coauthors) +
                     "\n -- Authors in exclude-list: "  + ", ".join(self.exclude_list) )

        for author in self.coauthors:
            t = Author(author, self.exclude_list, self.depth + 1)
            t.create_tree(publications)
            self.authors.append(t)


    """
        Once we have our Tree, we can call this recursive method to get the distance
        (the depth in our tree) between self.name_author and name_author
    """
    def get_depth(self,name_author):
        depths = []
        name_author = name_author.lower()

        for author in self.authors:

            # Get the depth from every author in self.authors if names match
            if author.name_author == name_author:
                depths.append(self.depth)

            # If names don't match, do a recursive call
            # on every author in self.authors
            else:
                sons_depths = author.get_depth(name_author)
                if sons_depths > 0:
                    depths.append(sons_depths)

        if len(depths) > 0:
            print(min(depths))
            return min(depths)
        else:
            return 0