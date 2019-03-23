import argparse
import os
import configparser
import datetime
import glob
from pdfrw import PdfWriter
from customFunctions import *


class Specification:

    def __init__(self, filename, stitch, clean, offset=0, page_lists=None):
        self.filename = filename
        self.stitch = stitch
        self.offset = offset
        self.clean = clean
        self.page_lists = page_lists if page_lists else [None]


def get_specification(filename):

    config = configparser.ConfigParser()
    config.read(filename)

    specifications = []

    for section in config.sections():

        filename_specification = config[section]['filename']
        stitch = int(config[section]['stitch'])
        clean = True if 'clean' in config[section] else False

        if '*' in filename_specification:
            documents_filenames = glob.glob(filename_specification)
        else:
            documents_filenames = [filename_specification]

        for document_filename in documents_filenames:

            offset = int(config[section]['offset'])
            page_ranges_raw = config[section]['pages']
            pages_list = []

            if page_ranges_raw:
                for page_range in page_ranges_raw.split('/'):

                    current_pages = []

                    for page_interval in page_range.split(','):

                        if '-' in page_interval:
                            start_page = offset + int(page_interval.split('-')[0])
                            end_page = offset + int(page_interval.split('-')[1])
                            for page_number in range(start_page - 1, end_page):
                                current_pages.append(page_number)
                        else:
                            current_pages.append(int(page_interval) + offset - 1)

                    pages_list.append(current_pages)
            else:

                pages_list = [None]

            specifications.append(Specification(document_filename, stitch, clean, offset, pages_list))

    return specifications


parser = argparse.ArgumentParser("Programa para generar pdfs imprimibles")
parser.add_argument("-min", "--minimal", action="store_true", help="generate minimal output, just one file per pdf")
args = parser.parse_args()

specifications_filename = "config.ini"
specifications = get_specification(specifications_filename)

output_dirname = "out"

if os.path.exists(output_dirname):
    output_dirname += datetime.datetime.now().strftime('_%H_%M_%d_%m_%Y')
    os.makedirs(output_dirname)
else:
    os.makedirs(output_dirname)

main_output = []
main_output_filename = os.path.join(output_dirname, "out.pdf")

for specification in specifications:

    document_output = []
    document_output_filename = os.path.join(output_dirname, specification.filename)

    for page_lists in specification.page_lists:

        page_range_output = make_booklet(specification.filename, specification.stitch, specification.clean, page_lists)

        if not args.minimal:
            PdfWriter(document_output_filename[:-4] + (('_' + '-'.join(str(i) for i in page_lists)) if page_lists else '') + '.pdf').addpages(page_range_output).write()
        document_output += page_range_output
        main_output += page_range_output

    PdfWriter(document_output_filename).addpages(document_output).write()

PdfWriter(main_output_filename).addpages(main_output).write()
