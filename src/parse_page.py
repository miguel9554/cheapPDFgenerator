import pdfrw
import codecs
from tika import parser


def print_page_content(filename, page):

    output_filename = '0'*(3-len(str(page))) + str(page) + '_' + filename[:3] + "out.txt"
    temp_filename = "temp_" + filename

    pdfrw.PdfWriter(temp_filename).addpage(pdfrw.PdfReader(filename).pages[page]).write()

    #raw = parser.from_file(temp_filename)

    with codecs.open(output_filename, "w", encoding='utf-8') as fp:
        fp.write(parser.from_file(temp_filename)['content'])
        # for key in raw:
        #     fp.write(str(key) + '\n')
        #     fp.write(str(raw[key]) + '\n' * 2)


def get_page_content(filename, page):

    output_filename = '0' * (3 - len(str(page))) + str(page) + '_' + filename[:3] + "out.txt"
    temp_filename = "temp_" + filename

    pdfrw.PdfWriter(temp_filename).addpage(pdfrw.PdfReader(filename).pages[page]).write()

    return parser.from_file(temp_filename)['content']


filename = "arq_ip.pdf"
pages = list(range(20))

for page in pages:
    print_page_content(filename, page)
