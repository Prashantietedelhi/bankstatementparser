import xlrd
import pandas as pd

import os,json


train_data_dir = "../AdditionalSpreading"
files = os.listdir(train_data_dir)
files = ["Birddogs-BofA-Bank-Statement-April.'17.xlsx"]
files = [os.path.join(train_data_dir, i) for i in files if ".xlsx" in i ]
# print(files)

key_pair = {}
for file in files:
    print(file)
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_index(1)
    rows, cols = (sheet.nrows,sheet.ncols)
    for i in range(cols):
        # for j in range(rows):
        print(0,i)
        print(1,i)
            # print(sheet.cell(j,i))
        if sheet.cell(1,i).value !='':
            key_pair[sheet.cell(0,i).value] = sheet.cell(1,i).value
# print(list(sheet.col(3)))


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
train_data = []
### Extract text from Images
for file in files:
    alltext = pytesseract.image_to_string(Image.open(file))
    alltext = alltext.split("\n")
    alltext = [i for i in alltext if i!='']
    for text in alltext:
        pdfData.append(text)
        li = []
        for key, val in key_pair.items():
            if str(val) in str(text):
                pos = text.find(str(val))
                endpos = pos+len(str(val))-1

                li.append((pos,endpos,key))
        if len(li)>0:
            train_data.append((text,{"entities":li}))
print(train_data)
    # print(text)

with open("training_data",'w') as f:
    json.dump(train_data,f)


import spacy
import random

nlp = spacy.blank('en')
optimizer = nlp.begin_training()

for i in range(20):
    random.shuffle(train_data)
    for text, annotations in train_data:
        nlp.update([text], [annotations], sgd=optimizer)

nlp.to_disk("model")
