from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract


filename = 'Birddogs-BofA-Bank-Statement-April.pdf'
newfilename = filename.replace(".pdf",'')

if os.path.isdir("working")==False:
    os.makedirs("working")

### Convert Pdf to Images
pages = convert_from_path('Birddogs-BofA-Bank-Statement-April.pdf')

### Save the Images
for pagenum, page in enumerate(pages):
    newfilename_temp = str(pagenum)+".jpg"
    page.save(os.path.join("working",newfilename_temp), 'JPEG')

files = list(os.listdir("working"))
files.sort(key=lambda f: int(f.replace(".jpg",'')))

files = [os.path.join("working",i) for i in files]
print(files)

pdfData = []
### Extract text from Images
for file in files:
    text = pytesseract.image_to_string(Image.open(file))
    # pdfData.append(text)
    text = text.split("\n")
    text = [i for i in  text if i!='']
    for t in text:
        print("==========",t)


