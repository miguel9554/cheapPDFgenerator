import csv
import argparse
from pdfrw import PdfWriter
from customFunctions import *
from glob import glob

parser = argparse.ArgumentParser("Programa para generar pdfs imprimibles")
parser.add_argument("-min", "--minimal", action="store_true", help="generate minimal output, just one file per pdf")
parser.add_argument("-ch", "--check", action="store_true", help="check if page contents are different")
args = parser.parse_args()

specifications = []

specifications_filename = "books.cfg"

with open(specifications_filename, "rt") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        specifications.append(row)

main_output = []
main_output_filename = "out.pdf"

for specification in specifications:

    filename_specification = specification[0]
    stitch = int(specification[1])

    if '*' in filename_specification:
        documents_filenames = glob(filename_specification)
    else:
        documents_filenames = [filename_specification]

    for document_filename in documents_filenames:

        document_output = []
        document_output_filename = "out." + document_filename
        offset = int(specification[2]) if len(specification) > 2 else '0'
        page_range_list = [] if len(specification) > 2 else [None]

        for i in range(3, len(specification)):

            page_range = []
            page_range_specification = specification[i]

            for page_number_specification in page_range_specification.split('+'):

                if '-' in page_number_specification:

                    start_page = offset + int(page_number_specification.split('-')[0])
                    end_page = offset + int(page_number_specification.split('-')[1])

                    for page_number in range(start_page - 1, end_page):

                        page_range.append(page_number)

                elif ',' in page_number_specification:

                    for page_number in page_number_specification.split(','):

                        page_range.append(int(page_number) + offset - 1)

                else:

                    page_range.append(int(page_number_specification))

            page_range_list.append(page_range)

        for page_range in page_range_list:

            page_range_output = make_booklet(document_filename, stitch, page_range)

            if not args.minimal:
                PdfWriter(document_output_filename[:-4] + (('_' + '-'.join(str(i) for i in page_range)) if page_range else '') + '.pdf').addpages(page_range_output).write()
            document_output += page_range_output
            main_output += page_range_output

        PdfWriter(document_output_filename).addpages(document_output).write()

PdfWriter(main_output_filename).addpages(main_output).write()
