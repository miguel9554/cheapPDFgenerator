import csv
from pdfrw import PdfWriter
from customFunctions import *
from glob import glob

documents = []

configFilename = "books.cfg"

with open(configFilename, "rt") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        documents.append(row)

mainOutput = []
MainOutDocumentName = "out.pdf"

for document in documents:

    if len(document) == 2:

        if '*' in document[0]:
            documents = glob(document[0])
        else:
            documents = [document[0] + ".pdf"]

        if document[1] == str(2):

            for doc in documents:
                currentOutDocumentName = "out." + doc
                currentOutput = make_2page_booklet(doc)
                mainOutput += currentOutput
                PdfWriter(currentOutDocumentName).addpages(currentOutput).write()

        elif document[1] == str(4):

            for doc in documents:
                currentOutDocumentName = "out." + doc
                currentOutput = make_4page_booklet(doc)
                mainOutput += currentOutput
                PdfWriter(currentOutDocumentName).addpages(currentOutput).write()

        elif document[1] == str(1):

            for doc in documents:
                currentOutDocumentName = "out." + doc
                currentOutput = PdfReader(doc).pages
                mainOutput += currentOutput
                PdfWriter(currentOutDocumentName).addpages(currentOutput).write()

        else:
            print(document[1])
            print("error")

        continue

    else:

        inDocumentName = document[0] + ".pdf"
        currentOutDocumentName = "out." + inDocumentName
        currentOutput = []
        offset = int(document[2])
        for i in range(3, len(document)):
            startPage = offset + int(document[i].split('-')[0])
            endPage = offset + int(document[i].split('-')[1])
            if document[1] == str(2):
                currentOutput += make_2page_booklet(inDocumentName, startPage, endPage)
            elif document[1] == str(4):
                currentOutput += make_4page_booklet(inDocumentName, startPage, endPage)
            elif document[1] == str(1):
                aux = PdfReader(inDocumentName).pages[startPage - 1: endPage]
                currentOutput += aux
                PdfWriter(currentOutDocumentName[:-4] + str(startPage) + ".pdf").addpages(aux).write()
            mainOutput += currentOutput
        PdfWriter(currentOutDocumentName).addpages(currentOutput).write()

PdfWriter(MainOutDocumentName).addpages(mainOutput).write()
