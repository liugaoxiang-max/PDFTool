import PyPDF2
import io
from PyPDF2 import PdfFileReader


with io.open('5.pdf', mode="rb") as f:
    input_pdf = PdfFileReader(f)
    media_box = input_pdf.getPage(0).mediaBox

min_pt = media_box.lowerLeft
max_pt = media_box.upperRight

pdf_width = max_pt[0] - min_pt[0]
pdf_height = max_pt[1] - min_pt[1]

print(pdf_width)
print(pdf_height)