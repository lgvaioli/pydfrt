import os
import sys
import argparse
import PyPDF2

class Command:
    # pdf_in: an opened pdf file pointer.
    # filename_out: the filename of the output file.
    # page_range: range of pages on which the command will operate. Pages start at 0.
    # even_degree: the degree to which even pages will be rotated. Negative
    # value indicates counterclockwise rotation.
    # odd_degree: the degree to which odd pages will be rotated.
    # all_degree: the degree to which all (i.e. even and odd) pages will be
    # rotated. If this value is not zero, the function will ignore even_degree
    # and odd_degree and use all_degree instead.
    def __init__(self, pdf_in, filename_out, page_range, even_degree, odd_degree, all_degree):
        self.filename_out = filename_out
        self.pdf_reader = PyPDF2.PdfFileReader(pdf_in)
        self.pdf_writer = PyPDF2.PdfFileWriter()
        self.page_range = page_range
        self.even_degree = even_degree
        self.odd_degree = odd_degree
        self.all_degree = all_degree
        self.all_degree = all_degree


    # Executes the command and writes a rotated output PDF named self.filename_out
    def execute(self):

        # First things first: create the output file
        try:
            pdf_out = open(self.filename_out, 'wb')

        except FileNotFoundError as err:
            print(err)
            sys.exit(-1)

        # Make a copy of the whole file
        i = 0
        last_page = self.pdf_reader.getNumPages() - 1
        while(i <= last_page):
            page = self.pdf_reader.getPage(i)
            self.pdf_writer.addPage(page)
            i += 1
        
        # Now we rotate whatever we need to rotate
        while(self.page_range[0] <= self.page_range[1]):
            page = self.pdf_reader.getPage(self.page_range[0])

            # all_degree takes precedence over even_ and odd_degree
            if self.all_degree > 0:
                page.rotateClockwise(self.all_degree)
            
            if self.all_degree < 0:
                page.rotateCounterClockwise(self.all_degree)

            # all_degree wasn't set
            if self.all_degree == 0:
                if not (self.page_range[0] + 1) % 2: # page is even
                    if(self.even_degree > 0):
                        page.rotateClockwise(self.even_degree)
                    elif(self.even_degree < 0):
                        page.rotateCounterClockwise(abs(self.even_degree))
                else: # page is odd
                    if(self.odd_degree > 0):
                        page.rotateClockwise(self.odd_degree)
                    elif(self.odd_degree < 0):
                        page.rotateCounterClockwise(abs(self.odd_degree))

            self.page_range[0] += 1

        # Write changes to output file and close it 
        self.pdf_writer.write(pdf_out)
        pdf_out.close()


    # For debugging purposes
    def debug_dump(self):
            print("[DEBUG] Printing Command object")
            print("  Output filename: " + self.filename_out)
            print("  Page range: " + str(self.page_range[0]) + "-" + str(self.page_range[1]))
            print("  Even degree: " + str(self.even_degree))
            print("  Odd degree: " + str(self.odd_degree))
            print("  All degree: " + str(self.all_degree))

# Parse arguments
parser = argparse.ArgumentParser(description="Pydfrt: A Python PDF rotator. Positive degrees (DEG) mean "
        "clockwise rotation; negative degrees mean counter-clockwise rotation. Degrees must be a multiple of "
        "90. Pages are counted starting from 1. In addition to a file, you must specify at least one of "
        "the following switches: -e, -o, -a. If the -a switch is specified, -e and -o are ignored. By default, "
        "all pages will be rotated, unless you specify a page range with -pp, or a single page with -p.")
parser.add_argument("file", help="input filename")
parser.add_argument("-fo", "--fileout", metavar="NAME", help="output filename. By default, '_rotated' is appended "
        "to the input filename. If you specify an output filename and forget to add '.pdf', the program adds it for you")
group = parser.add_mutually_exclusive_group()
group.add_argument("-p", "--page", metavar="N", help="single page to be rotated", type=int)
group.add_argument("-pp", "--pagerange", metavar="N", help="range of pages to be rotated", nargs=2, type=int)
parser.add_argument("-e", "--even", metavar="DEG", help="rotate even pages", type=int)
parser.add_argument("-o", "--odd", metavar="DEG", help="rotate odd pages", type=int)
parser.add_argument("-a","--all", metavar="DEG", help="rotate all (i.e. even and odd) pages", type=int)
args = parser.parse_args()
 

# Try to open input file
try:
    pdf_file = open(args.file, 'rb')

except FileNotFoundError as err:
    print(err)
    sys.exit(-1)

# Prepare PDF reader
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
num_pages = pdf_reader.getNumPages()

# Check and set page range 
if(args.pagerange):

    if(args.pagerange[0] <= 0):
        print("Error: pages start at 1. Aborting")
        sys.exit(-1)

    if(args.pagerange[1] < args.pagerange[0] or args.pagerange[1] > num_pages):
        print("Error: invalid page range. Aborting")
        sys.exit(-1)

    page_range = [args.pagerange[0] - 1, args.pagerange[1] - 1]

elif(args.page):

    if(args.page <= 0 or args.page > num_pages):
        print("Error: invalid page. Aborting")
        sys.exit(-1)
    else:
        page_range = [args.page-1, args.page-1]

else: # neither a range nor a single page was set: set range to all pages
    page_range = [0, num_pages - 1]

# Check and set rotation degrees
if not (args.even or args.odd or args.all):
    print("Error: at least one of the following switches must be specified: -e, -o, -a. Aborting")
    sys.exit(-1)

if(args.even):
    if(args.even % 90 != 0):
        print("Error: even degree must be a multiple of 90. Aborting")
        sys.exit(-1)
else:
    args.even = 0

if(args.odd):
    if(args.odd % 90 != 0):
        print("Error: odd degree must be a multiple of 90. Aborting")
        sys.exit(-1)
else:
    args.odd = 0

if(args.all):
    if(args.all % 90 != 0):
        print("Error: all degree must be a multiple of 90. Aborting")
        sys.exit(-1)
else:
    args.all = 0

# Check and set output filename
if not(args.fileout):
    args.fileout = os.path.splitext(args.file)[0] + "_rotated.pdf"
elif(os.path.splitext(args.fileout) != ".pdf"):
    args.fileout += ".pdf"


# Construct and execute command
command = Command(pdf_file, args.fileout, page_range, args.even, args.odd, args.all)
command.execute()

# Close input file
pdf_file.close()

