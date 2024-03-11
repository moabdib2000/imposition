# see https://stackoverflow.com/questions/51973437/reverse-pdf-imposition
# based on Yury Kirienko and Shrinivasan T works

# A little project for learn Python finding a solution for imposition files for my little printshop


import copy
import sys
import math
from pypdf import PdfReader

"""
Reverse imposing:

--A3--         --A4--
[12| 1]         [1]
[ 2|11]         [2]
[10| 3]    =>   [3]
  ...           ...
[ 6| 7]         [6]
                [7]
                ...
               [12]

"""

def split_pages(src, dst):
    src_f = file(src, 'r+b')
    dst_f = file(dst, 'w+b')

    input_PDF = pyPdf.PdfFileReader(src_f)
    num_pages = input_PDF.getNumPages()
    
    first_half, second_half = [], []

    for i in range(num_pages):
        p = input_PDF.getPage(i)
        q = copy.copy(p)
        q.mediaBox = copy.copy(p.mediaBox)

        x1, x2 = p.mediaBox.lowerLeft
        x3, x4 = p.mediaBox.upperRight

        x1, x2 = math.floor(x1), math.floor(x2)
        x3, x4 = math.floor(x3), math.floor(x4)
        x5, x6 = math.floor(x3/2), math.floor(x4/2)

        if x3 > x4:
            # horizontal
            p.mediaBox.upperRight = (x5, x4)
            p.mediaBox.lowerLeft = (x1, x2)

            q.mediaBox.upperRight = (x3, x4)
            q.mediaBox.lowerLeft = (x5, x2)
        else:
            # vertical
            p.mediaBox.upperRight = (x3, x4)
            p.mediaBox.lowerLeft = (x1, x6)

            q.mediaBox.upperRight = (x3, x6)
            q.mediaBox.lowerLeft = (x1, x2)

    
        if i in range(1,num_pages+1,2):
            first_half += [p]
            second_half += [q]
        else:
            first_half += [q]
            second_half += [p]

    output = pyPdf.PdfFileWriter()
    for page in first_half + second_half[::-1]:
        output.addPage(page)

    output.write(dst_f)
    src_f.close()
    dst_f.close()

if len(sys.argv) < 3:
    print("\nusage:\n$ python reverse_impose.py input.pdf output.pdf")
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

split_pages(input_file,output_file)
