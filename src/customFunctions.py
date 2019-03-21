from pdfrw import PdfReader, PageMerge


def make_2page_booklet(filename, pages=None):

    blankPDF_filename = "src/blank.pdf"
    blankPDF = PdfReader(blankPDF_filename).pages[0]
    input_pages = PdfReader(filename).pages

    if not pages:
        pages = [i for i in range(len(input_pages))]

    aux = [input_pages[i] for i in pages]
    input_pages = aux  # check if it is possible to avoid aux
    output_pages = []

    inputImpairPages = len(pages) % 2
    if inputImpairPages:
        outputImpairPages = ((len(pages)+1)/2) % 2
    else:
        outputImpairPages = (len(pages)/2) % 2

    while len(input_pages) >= 2:
        output_pages.append(side_by_side_page(input_pages.pop(0), input_pages.pop(0)))
    if inputImpairPages:
        output_pages.append(side_by_side_page(input_pages.pop(0), blankPDF))
    if outputImpairPages:
        output_pages.append(blankPDF)

    return output_pages


def make_4page_booklet(filename, pages=None):

    blankPDF_filename = "src/blank.pdf"
    blankPDF = PdfReader(blankPDF_filename).pages[0]
    input_pages = PdfReader(filename).pages

    if not pages:
        pages = [i for i in range(len(input_pages))]

    number_output_pages = -(-len(pages) // 4)   # divison by 4 rounded up
    output_impair_pages = number_output_pages % 2

    aux = [input_pages[i] for i in pages]
    input_pages = aux       # check if it is possible to avoid aux
    output_pages = []

    for index in range(0, len(input_pages) - len(input_pages) % 4, 4):
        output_pages.append(get4(input_pages[index:index + 4]))

    if len(input_pages) % 4:
        aux = input_pages[len(input_pages) - len(input_pages) % 4:len(input_pages)]
        for i in range((4 - len(input_pages) % 4)):
            aux.append(blankPDF)
        output_pages.append(get4(aux))

    if output_impair_pages:
        output_pages.append(blankPDF)

    return output_pages


def make_1page_booklet(filename, pages=None):

    blankPDF_filename = "src/blank.pdf"
    blankPDF = PdfReader(blankPDF_filename).pages[0]
    input_pages = PdfReader(filename).pages

    if not pages:
        pages = [i for i in range(len(input_pages))]

    output_pages = []

    for page_idx in pages:
        output_pages.append(PdfReader(filename).pages[page_idx])
    if len(pages) % 2:
        output_pages.append(blankPDF)

    return output_pages


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
