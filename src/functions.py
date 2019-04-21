import pdfrw
import tempfile
import uuid
import os
from tika import parser


def clean_file(filename, out_filename):

    pages = list(range(len(pdfrw.PdfReader(filename).pages)))
    input_file = pdfrw.PdfReader(filename)

    output_pages = []

    current_content = ''
    old_content = ''

    with tempfile.TemporaryDirectory() as tmpdirname:

        for page in pages:

            temp_filename = os.path.join(tmpdirname, str(uuid.uuid4()))
            pdfrw.PdfWriter(temp_filename).addpage(input_file.pages[page]).write()

            current_content = parser.from_file(temp_filename)['content']

            if current_content != old_content:
                output_pages.append(input_file.pages[page])
            else:
                output_pages.pop()
                output_pages.append(input_file.pages[page])

            old_content = current_content

    pdfrw.PdfWriter(out_filename).addpages(output_pages).write()


def get_page_content(filename, page):

    output_filename = '0' * (3 - len(str(page))) + str(page) + '_' + filename[:3] + "out.txt"
    temp_filename = "temp_" + filename

    pdfrw.PdfWriter(temp_filename).addpage(pdfrw.PdfReader(filename).pages[page]).write()

    return parser.from_file(temp_filename)['content']


def make_booklet(filename, stitch, clean, pages=None):

    tmp_filename = str(uuid.uuid4())

    if clean:
        clean_file(filename, tmp_filename)
        input_pages = pdfrw.PdfReader(tmp_filename).pages
    else:
        input_pages = pdfrw.PdfReader(filename).pages

    if not pages:
        pages = [i for i in range(len(input_pages))]

    number_output_pages = -(-len(pages) // stitch)   # divison by 4 rounded up
    output_impair_pages = number_output_pages % 2

    aux = [input_pages[i] for i in pages]
    input_pages = aux       # check if it is possible to avoid aux
    output_pages = []

    for index in range(0, len(input_pages) - len(input_pages) % stitch, stitch):
        if stitch == 4:
            output_pages.append(get4(input_pages[index:index + 4]))
        elif stitch == 2:
            output_pages.append(side_by_side_page(input_pages[index], input_pages[index + 1]))
        elif stitch == 1:
            output_pages.append(input_pages[index])
        else:
            exit("ERROR: invalid stitch")

    if len(input_pages) % stitch:

        if stitch == 4:

            aux = input_pages[len(input_pages) - len(input_pages) % 4:len(input_pages)]

            blank_pdf = pdfrw.PdfReader(filename).pages[len(input_pages) - 1]
            blank_pdf['/Contents'].stream = ""

            for i in range(4 - len(input_pages) % 4):
                aux.append(blank_pdf)

            output_pages.append(get4(aux))

        elif stitch == 2:

            blank_pdf = pdfrw.PdfReader(filename).pages[len(input_pages) - 1]
            blank_pdf['/Contents'].stream = ""

            output_pages.append(side_by_side_page(input_pages[(len(input_pages)-1)], blank_pdf))

    if output_impair_pages:

        if stitch == 4:

            blank_pdf = get4(pdfrw.PdfReader(filename).pages[len(input_pages) - 5:len(input_pages) - 1])
            blank_pdf['/Contents'].stream = ""
            output_pages.append(blank_pdf)

        elif stitch == 2:

            blank_pdf = pdfrw.PdfReader(filename).pages[len(input_pages) - 1]
            blank_pdf['/Contents'].stream = ""

            output_pages.append(side_by_side_page(blank_pdf, blank_pdf))

    if clean:
        os.remove(tmp_filename)

    return output_pages


def get4(srcpages):
    scale = 0.5
    srcpages = pdfrw.PageMerge() + srcpages
    x_increment, y_increment = (scale * i for i in srcpages.xobj_box[2:])
    for i, page in enumerate(srcpages):
        page.scale(scale)
        page.x = x_increment if i & 1 else 0
        page.y = 0 if i & 2 else y_increment
    return srcpages.render()


def side_by_side_page(page_left, page_right):

    result = pdfrw.PageMerge() + [page_left, page_right]
    result[1].x += result[0].w  # Start second page after width of first page.
    return result.render()
