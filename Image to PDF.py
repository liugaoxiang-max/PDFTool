import PIL
from PIL import Image
from PIL import PdfImagePlugin

#image1 = Image.open('\img\page_5_signed.jpg')
image1 = Image.open("D:/script/python/projects/PDFTool/Material/Image\\page_5.jpg")
im1 = image1.convert('RGB')
im1.save('6.pdf',resolution=200)