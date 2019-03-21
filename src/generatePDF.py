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
        docOutput = []
        offset = int(document[2])
        for i in range(3, len(document)):

            currentOutput = []
            page_range = document[i]
            temp_page_range = []

            for curent_page_range in page_range.split('+'):
                if '-' in curent_page_range:
                    startPage = offset + int(curent_page_range.split('-')[0])
                    endPage = offset + int(curent_page_range.split('-')[1])
                    for page_number in range(startPage-1, endPage):
                        temp_page_range.append(page_number)
                elif ',' in curent_page_range:
                    for inner_page in curent_page_range.split(','):
                        temp_page_range.append(int(inner_page) + offset - 1)
                else:
                    temp_page_range.append(int(curent_page_range))

            page_range = temp_page_range

            if document[1] == str(2):
                currentOutput += make_2page_booklet(inDocumentName, page_range)
            elif document[1] == str(4):
                currentOutput += make_4page_booklet(inDocumentName, page_range)
            elif document[1] == str(1):
                currentOutput += make_1page_booklet(inDocumentName, page_range)

            PdfWriter(currentOutDocumentName[:-4] + '_' + document[i] + '.pdf').addpages(currentOutput).write()
            docOutput += currentOutput
            mainOutput += currentOutput

        PdfWriter(currentOutDocumentName).addpages(docOutput).write()

PdfWriter(MainOutDocumentName).addpages(mainOutput).write()
