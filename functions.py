from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
from pathlib import Path
import pdf2image
from PIL import Image, PdfImagePlugin


class PdfImgFunctions:
    def __init__(self, file_list, out_folder, to_format, dpi):
        self.file_list = file_list
        self.out_folder = out_folder
        self.to_format = to_format

    def PDFMerge(self, file_list, out_folder):
        merger = PdfFileMerger()
        for pdf in file_list:
            merger.append(pdf)
        merger.write(f"{out_folder}\\result.pdf")
        merger.close()

    def PDFSplit(self, file_list, out_folder):
        inputpdf = PdfFileReader(open(file_list, "rb"))
        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open(f"{out_folder}\\page_%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)

    def PDFtoImg(self, file_list, out_folder, to_format):
        def Job():
            pdf2image.convert_from_path(
                PDF_PATH,
                #dpi=dpi,
                output_folder=out_folder,
                #first_page=None,
                #last_page=None,
                fmt=to_format,
                thread_count=1,
                #userpw=USERPWD,
                #use_cropbox=USE_CROPBOX,
                #strict=STRICT
            )

        if isinstance(file_list, list):
            for EachFile in file_list:
                PDF_PATH = EachFile
                Job()
        else:
            PDF_PATH = file_list
            Job()

    def ImgtoPDF(self, file_list, out_folder, dpi):
        dpi = int(dpi)
        Index = 1

        def Job():
            image1 = Image.open(Img_PATH)
            im1 = image1.convert('RGB')
            im1.save(f'{self.out_folder}\\page_{Index}.pdf', resolution=dpi)

        if isinstance(file_list, list):
            for EachFile in file_list:
                Img_PATH = EachFile
                Job()
                Index += 1
        else:
            Img_PATH = file_list
            Job()
