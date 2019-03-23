import configparser
import glob


class Specification:

    def __init__(self, filename, stitch, offset=0, page_lists=None):
        self.filename = filename
        self.stitch = stitch
        self.offset = offset
        self.page_lists = page_lists



config_filename = "config.ini"
config = configparser.ConfigParser()
config.read(config_filename)

specifications = []

for section in config.sections():

    filename_specification = config[section]['filename']
    stitch = int(config[section]['stitch'])

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
            pages_list = None

        specifications.append(Specification(document_filename, stitch, offset, pages_list))

for spec in specifications:
    print("archivo: {}".format(spec.filename))
    print('\t' + "offset: {}".format(spec.offset))
    print('\t' + "stitch: {}".format(spec.stitch))
    print('\t' + "intervals: {}".format(spec.page_lists))
