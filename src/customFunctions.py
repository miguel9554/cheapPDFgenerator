from pdfrw import PdfReader, PageMerge


def make_2page_booklet(filename, initPage=1, endPage=None):

    blakPDFfilename = "blank.pdf"
    blankPDF = PdfReader(blakPDFfilename).pages[0]
    ipages = PdfReader(filename).pages

    if not endPage:
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


def make_4page_booklet(filename, initPage=1, endPage=None):

    blakPDFfilename = "blank.pdf"
    blankPDF = PdfReader(blakPDFfilename).pages[0]
    ipages = PdfReader(filename).pages

    if not endPage:
        endPage = len(ipages)

    outputImpairPages = (endPage - initPage) // 4 + (endPage - initPage) % 4

    ipages = ipages[initPage - 1:endPage]
    opages = []

    for index in range(0, len(ipages), 4):
        opages.append(get4(ipages[index:index + 4]))

    if outputImpairPages:
        opages.append(blankPDF)

    return opages


def get4(srcpages):
    scale = 0.5
    srcpages = PageMerge() + srcpages
    x_increment, y_increment = (scale * i for i in srcpages.xobj_box[2:])
    for i, page in enumerate(srcpages):
        page.scale(scale)
        page.x = x_increment if i & 1 else 0
        page.y = 0 if i & 2 else y_increment
    return srcpages.render()


def side_by_side_page(page_left, page_right):

    result = PageMerge() + [page_left, page_right]
    result[1].x += result[0].w  # Start second page after width of first page.
    return result.render()
