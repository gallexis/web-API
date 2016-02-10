__author__ = 'alexisgallepe'
import xml.sax
from datetime import date

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

        except Exception as e:
            print(e)
            pass

    def endElement(self, name):
        try:

            if self.publicationBalise == name:
                self.publicationBalise = ""

                self.publication["authors"] = self.authors

                # if (2016 - 5) <= 2001  ---> False
                if not self.publication["year"] == '' and (date.today().year - self.last_years_wanted) <= int(self.publication["year"]):
                    self.publications.append(self.publication)
                    self.publication = {"authors":[], "title":"", "year":"", "journal":"","booktitle":""}

                self.authors = []

            if self.fieldBalise == name:
                self.fieldBalise = ""

        except Exception as e:
            print(e)
            pass


    def characters(self, content):
        try:
            if not self.publicationBalise == "" and self.fieldBalise == "author":
                self.authors.append(content)

            if not self.fieldBalise == "" and not self.fieldBalise == "author":
                self.publication[self.fieldBalise] = content

        except Exception as e:
            print(e)
            pass