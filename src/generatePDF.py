import csv
import sys
from pdfrw import PdfReader, PdfWriter, PageMerge


def side_by_side_page(page_left, page_right):
    result = PageMerge() + [page_left, page_right]
    result[1].x += result[0].w  # Start second page after width of first page.
    return result.render()


def make_booklet(filename, initPage=1, endPage=None):

    """First page, pairs of pages, last page."""
    blakPDFfilename = "blank.pdf"
    blankPDF = PdfReader(blakPDFfilename).pages[0]
    ipages = PdfReader(filename).pages
    if endPage == None:
        endPage = len(ipages)
    ipages = ipages[initPage-1:endPage]
    opages = []
    inputImpairPages = (endPage-initPage+1) % 2
    if inputImpairPages:
        outputImpairPages = ((endPage-initPage+2)/2) % 2
    else:
        outputImpairPages = ((endPage-initPage+1)/2) % 2
    while len(ipages) >= 2:
        opages.append(side_by_side_page(ipages.pop(0), ipages.pop(0)))
    if inputImpairPages:
        opages.append(side_by_side_page(ipages.pop(0), blankPDF))
    if outputImpairPages:
        opages.append(blankPDF)
    return opages


documents = []

configFilename, = sys.argv[1:]

with open(configFilename, "rt") as csvfile:
    reader = csv.reader(csvfile, delimiter = ' ')
    for row in reader:
        documents.append(row)

mainOutput = []
MainOutDocumentName = "out.pdf"

for document in documents:
    inDocumentName = document[0] + ".pdf"
    currentOutDocumentName = "out." + inDocumentName
    if len(document) == 1:
        currentOutput = make_booklet(inDocumentName)
        mainOutput += currentOutput
        PdfWriter(currentOutDocumentName).addpages(currentOutput).write()
        continue
    currentOutput = []
    offset = int(document[1])
    for i in range(2, len(document)):
        startPage = offset + int(document[i].split('-')[0])
        endPage = offset + int(document[i].split('-')[1])
        currentOutput += make_booklet(inDocumentName, startPage, endPage)
        mainOutput += currentOutput
    PdfWriter(currentOutDocumentName).addpages(currentOutput).write()
PdfWriter(MainOutDocumentName).addpages(mainOutput).write()
