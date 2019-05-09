import xlrd
import pandas as pd

import os,json
from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract
import shutil

folder = "working"
if os.path.isdir("working")==False:
    os.makedirs("working")

for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

train_data_dir = "../AdditionalSpreading"

files = os.listdir(train_data_dir)

files = [os.path.join(train_data_dir, i) for i in files ]
pdffile_map =  {}
print(files)
for f in files:
    if ".pdf" in f:
        pdffile_map[f] = f.replace(".pdf",".xlsx")
print(pdffile_map)
# for file in files:
train_data = []
# pdffile_map={}
key_pair = {}
alltext_all=[]
# pdffile_map[r"../AdditionalSpreading/Birddogs-BofA-Bank-Statement-April.'17.pdf"]=r"../AdditionalSpreading/Birddogs-BofA-Bank-Statement-April.'17.xlsx"
for pdfFile, excelFile in pdffile_map.items():
    newfilename = pdfFile.replace(".pdf", '')
    # excelFile = xlrd.open_workbook(excelFile)
    # key_pair = {}

    # wb = xlrd.open_workbook(excelFile)
    # sheet = wb.sheet_by_index(1)
    # rows, cols = (sheet.nrows, sheet.ncols)
    # for i in range(cols):
    #     # for j in range(rows):
    #     # print(0, i)
    #     # print(1, i)
    #     # print(sheet.cell(j,i))
    #     if sheet.cell(1, i).value != '':
    #         try:
    #             key_pair[sheet.cell(0, i).value].append(sheet.cell(1, i).value)
    #         except:
    #             key_pair[sheet.cell(0, i).value] = []
    #             key_pair[sheet.cell(0, i).value].append(sheet.cell(1, i).value)


    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    pages = convert_from_path(pdfFile)
    for pagenum, page in enumerate(pages):
        newfilename_temp = str(pagenum) + ".jpg"
        page.save(os.path.join("working", newfilename_temp), 'JPEG')

    files = list(os.listdir("working"))
    files.sort(key=lambda f: int(f.replace(".jpg", '')))

    files = [os.path.join("working", i) for i in files]
    print(files)

    pdfData = []

    ### Extract text from Images
    for file in files:
        alltext = pytesseract.image_to_string(Image.open(file))
        alltext = alltext.split("\n")
        alltext = [i for i in alltext if i != '']
        # print(len(alltext))
        # alltext = list(set(alltext))
        # print(len(alltext))
        alltext_all.extend(alltext)
    print(len(alltext_all))
    # alltext_all = list(set(alltext_all))
    # print((alltext_all))


    # for text in alltext_all:
    #     pdfData.append(text)
    #     li = []
    #     for key, val in key_pair.items():
    #         if str(val) in str(text):
    #             pos = text.find(str(val))
    #             endpos = pos + len(str(val)) - 1
    #
    #             li.append((pos, endpos, key))
    #     if len(li) > 0:
    #         train_data.append((text, {"entities": li}))


# print(key_pair)
# useditems= ["Account#","Acctholdername","Accttype","Acctownership","Nameofbank","BankAddress","BankAddress","BankAddress"]
# for k, v in key_pair.items():
#     if k in useditems:
#         v = list(set(v))
#         with open(k+".txt","w") as f:
#             for i in v:
#                 f.write(i+"\n")

with open("Logs.txt","w") as f:
    for i in alltext_all:
        f.write(i+"\n")

# with open("training_data",'w') as f:
#     json.dump(train_data,f)