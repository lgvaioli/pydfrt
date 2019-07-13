import os
import sys
import re
import PyPDF2

class Command:
    # pdf_in: an opened pdf file pointer.
    # filename_out: the filename of the output file.
    # page_range: range of pages on which the command will operate.
    # even_degree: the degree to which even pages will be rotated. Negative
    # value indicates counterclockwise rotation.
    # odd_degree: you guess big boy.
    def __init__(self, pdf_in, filename_out, page_range, even_degree, odd_degree):
        self.filename_out = filename_out
        self.pdf_reader = PyPDF2.PdfFileReader(pdf_in)
        self.pdf_writer = PyPDF2.PdfFileWriter()
        self.page_range = page_range # starts at 0

        if(even_degree % 90) != 0:
            print("Error: degrees must be a multiple of 90; setting even degree to 0")
            self.even_degree = 0
        else:
            self.even_degree = even_degree

        if(odd_degree % 90) != 0:
            print("Error: degrees must be a multiple of 90; setting odd degree to 0")
            self.odd_degree = 0
        else:
            self.odd_degree = odd_degree

    # Executes the command and writes a rotated output PDF named self.filename_out
    def execute(self):
        page_num = self.page_range[0]
        page_end = self.page_range[1]

        while(page_num <= page_end):
            page = self.pdf_reader.getPage(page_num)

            if not (page_num + 1) % 2: # page is even
                if(self.even_degree > 0):
                    page.rotateClockwise(self.even_degree)
                else:
                    page.rotateCounterClockwise(abs(self.even_degree))
            else: # page is odd
                if(self.odd_degree > 0):
                    page.rotateClockwise(self.odd_degree)
                else:
                    page.rotateCounterClockwise(abs(self.odd_degree))

            self.pdf_writer.addPage(page)
            page_num += 1

        try:
            pdf_out = open(self.filename_out, 'wb')

        except FileNotFoundError as err:
            print(err)
            sys.exit(-1)

        self.pdf_writer.write(pdf_out)
        pdf_out.close()


    # For debugging purposes
    def display(self):
        print("[DEBUG] Printing Command object")
        print("  Output filename: " + self.filename_out)
        print("  Page range: " + str(self.page_range[0]) + "-" + str(self.page_range[1]))
        print("  Even degree: " + str(self.even_degree))
        print("  Odd degree: " + str(self.odd_degree))


# Check command line
if(len(sys.argv) != 3):
    print("Usage: python " + sys.argv[0] + " filename \"commands_str\"")
    sys.exit(-1)


# Try to open file specified in first argument
try:
    pdf_file = open(sys.argv[1], 'rb')

except FileNotFoundError as err:
    print(err)
    sys.exit(-1)

# Build output filename
filename_out = os.path.splitext(sys.argv[1])[0] + "_ROTATED.pdf"

# All pages
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
page_range = [0, pdf_reader.getNumPages() - 1]


# Parse commands string.
# Commands string format: [range] (e [-]deg, o [-]deg); [range]...
comms = re.sub(' +', ' ', sys.argv[2]) # remove duplicate whitespace
comms = comms.split("; ");

for i in comms:
    # Remove duplicate whitespace.
    i = re.sub(' +', ' ', i)

    print("\nCommand string: " + i)

    # FIXME: implement range parsing

    i  = i.split(", ");

    even_command = i[0][1:] # = "e [-]deg"
    odd_command = i[1][:-1] # = "o [-]deg"

    #print("[DEBUG] even_command: " + even_command)
    #print("[DEBUG] odd_command: " + odd_command)

    even_degree = int(even_command.split(" ")[1])
    odd_degree = int(odd_command.split(" ")[1])

    #print("[DEBUG] even_degree: " + str(even_degree))
    #print("[DEBUG] odd_degree: " + str(odd_degree))

    # Construct and execute command
    command = Command(pdf_file, filename_out, page_range, even_degree, odd_degree)
    command.display()
    command.execute()


pdf_file.close()

