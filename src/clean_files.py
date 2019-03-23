import pdfrw
import tempfile
import uuid
import os
from tika import parser


def clean_file(filename, out_filename):

    pages = list(range(len(pdfrw.PdfReader(filename).pages)))
    input_file = pdfrw.PdfReader(filename)

    output_pages = []

    content = ''
    old_content = ''

    with tempfile.TemporaryDirectory() as tmpdirname:

        for page in pages:

            temp_filename = os.path.join(tmpdirname, str(uuid.uuid4()))
            pdfrw.PdfWriter(temp_filename).addpage(input_file.pages[page]).write()
            content = parser.from_file(temp_filename)['content']
            if content != old_content:
                output_pages.append(input_file.pages[page])
            old_content = content

    pdfrw.PdfWriter(out_filename).addpages(output_pages).write()
