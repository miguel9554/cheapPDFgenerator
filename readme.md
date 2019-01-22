The goal of this project is to make a command line program for generation of pdf files ready for printing, providing the original pdf files and specifications.

This implementation is done in python with the use of the library pdfrw (https://github.com/pmaupin/pdfrw)


********************

Idea of the program: you have multiple files, you want to print certain intervals of them, and you want the intervals to be stiched 2 pages into 1 or 4 pages into 1.
You can specifiy then, files, and for each files intervals to be printed and if they have to be stiched 4 to 1, 2 to 1 or leaved as they are. It is common for pdf files to
have the file page numbering and the "real" numbering with an offset, so you can specifiy this offset too and refer to the intervals with their "real" numeration (the one that
appears in the pages of the book and on the index).
The programs deals with putting a blank file on intervals that are uneven, so when you print them, you dont get a first page of an interval into another.

********************

********************

considerations to run the program:

the command to run the program is "python generatePDF.py" (or python src/generatePDF.py if you run the program from the main folder)
books.cfg, a 1-page blank pdf file blank.pdf and all of the files to process should be in the directory where the python script is runned


********************


books.cfg format:

<filename> <formnat> <offset> <range1> <range2> ... <rangeN>

this converts filename from "offset" page to N intervals specified in "rangeI", with range as "startPage-endPage", using "format" original pages per output page

example:

grayMeyer 2 16 78-168 169-250
schaum 4

this takes the range specified in the grayMeyer line, converts them taking into account the offset, joins them and makes an individual file named grayMeyer.out, stiching 2 pages in 1
in the case of schaum, as no offset or interval is specified, the whole document is converted stiching 4 pages to 1


*****

improvements:

-redefine books.cfg format to be used with argparse lib from python std lib
-separated modules for reading arguments and generating the files (currently badly hard-coded (if len == 2...))
-make blank pdf part of the program so it can be made a standalone .exe (otherwise, appart from the .exe file blank.pdf will be needed) (a possibility, with py2exe using data_files)