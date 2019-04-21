The goal of this project is to make a command line program for generation of pdf files ready for printing, providing the original pdf files and specifications.  
  
This implementation is done in python with the use of the library pdfrw (https://github.com/pmaupin/pdfrw)  
  
  
********************  
  
Idea of the program: you have multiple files, you want to print certain intervals of them, and you want the intervals to be stiched 2 pages into 1 or 4 pages into 1.  
You can specifiy then, files, and for each files intervals to be printed and if they have to be stiched 4 to 1, 2 to 1 or leaved as they are. It is common for pdf files to  
have the file page numbering and the "real" numbering with an offset, so you can specifiy this offset too and refer to the intervals with their "real" numeration (the one that  
appears in the pages of the book and on the index).  
The programs deals with putting a blank file on intervals that are uneven, so when you print them, you dont get a first page of an interval into another.  
  
********************  
  
Requirements to ru the program:  
  
-Python 3  
-tika module  
-pdfrw module  
  
********************  
  
How to run the program:  
  
the command to run the program is "python pdfp.py" (or python src/generatePDF.py if you run the program from the main folder).  
config.ini should be where you are running the script  
  
  
********************  
  
  
config.ini format:  
  
[id] --------------------> identifier for each specification, can be anything, for safety make it an increasing list of integers  
  
filename = arq_ip.pdf ---> name of the file, or regular expression to process many files with the same configuration  
stitch = 4 --------------> pages to be stitched  
offset = 0 --------------> offset in the number of pages  
clean = True ------------> make it true to ommit pages with the same content, for normal processing make it false or dont include it  
pages =  ----------------> intervals, separated by '/', and each intervals separates pages by ',', a dash '-' indicates continuos pages  
	example:  

	pages = 1-5/6,7,11,13-15 ---> 2 page intervals, first one [1,2,3,4,5], second one [6,7,11,13,14,15]  
	to include all pages, leave the field empty (pages = )  
