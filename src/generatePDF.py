import csv
from pdfrw import PdfWriter
from customFunctions import *

documents = []

configFilename = "books.cfg"

with open(configFilename, "rt") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        documents.append(row)

mainOutput = []
MainOutDocumentName = "out.pdf"

for document in documents:
    inDocumentName = document[0] + ".pdf"
    currentOutDocumentName = "out." + inDocumentName
    if len(document) == 2:
        if document[1] == str(2):
            currentOutput = make_2page_booklet(inDocumentName)
        elif document[1] == str(4):
            currentOutput = make_4page_booklet(inDocumentName)
        else:
            print(document[1])
            print("error")
        mainOutput += currentOutput
        PdfWriter(currentOutDocumentName).addpages(currentOutput).write()
        continue
    currentOutput = []
    offset = int(document[1])
    for i in range(3, len(document)):
        startPage = offset + int(document[i].split('-')[0])
        endPage = offset + int(document[i].split('-')[1])
        if document[1] == 2:
            currentOutput += make_2page_booklet(inDocumentName, startPage, endPage)
        elif document[1] == 4:
            currentOutput += make_4page_booklet(inDocumentName, startPage, endPage)
        mainOutput += currentOutput
    PdfWriter(currentOutDocumentName).addpages(currentOutput).write()

PdfWriter(MainOutDocumentName).addpages(mainOutput).write()
