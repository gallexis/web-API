__author__ = 'alexisgallepe'
import xml.sax
from datetime import date
try:
    import cPickle as pickle
except:
    import pickle

class XmlParser(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()

        self.last_years_wanted = 0

        self.publicationBalise = ""
        self.fieldBalise = ""

        self.publications_index = ["article","inproceedings","proceedings","book","incollection","phdthesis","masterthesis"]
        self.fields_index = ["author", "title", "year", "journal","booktitle"]

        self.publication = {"authors":[], "title":"", "year":"", "journal":"","booktitle":""}
        self.publications = []

        self.authors = []

    def parse(self, sourceFileName, last_years_wanted):
        self.last_years_wanted = last_years_wanted
        source = open(sourceFileName)
        xml.sax.parse(source, self)

    def startElement(self, name, attrs):
        try:
            if name in self.publications_index:
                self.publicationBalise = name

            if name in self.fields_index:
                self.fieldBalise = name

        except:
            pass

    def endElement(self, name):
        try:

            if self.publicationBalise == name:
                self.publicationBalise = ""

                self.publication["authors"] = self.authors

                # if (2016 - 5) <= 2011  ---> False
                if not self.publication["year"] == '' and (date.today().year - self.last_years_wanted) <= int(self.publication["year"]):
                    self.save_binaryMode(self.publication)

                self.authors = []

            if self.fieldBalise == name:
                self.fieldBalise = ""

        except:
            pass

    def save_binaryMode(self,publication):
        with open("publications.bin",'ab') as fp:
            try:
                pickle.dump(publication,fp,pickle.HIGHEST_PROTOCOL)
                self.publication = {"authors":[], "title":"", "year":"", "journal":"","booktitle":""}

            except Exception as e:
                print("error save_binaryMode: ",e)

    def read_binaryMode(self,file):
        with open(file,'rb') as fp:
            while True:
                try:
                    self.publications.append(pickle.load(fp))
                except EOFError:
                    break