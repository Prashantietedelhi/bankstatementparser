import json

data = json.load(open("training_data"))
newdata = []
for d in data:
    li = d[1]['entities']
    # li = [i for i in li if i[2]!='Acctownership' and i[2]!='Acctholdername' and i[2]!='BankState' and i[2]!='Checksum']
    li = [i for i in li if i[2]=='Nameofbank' and i[2]!='BankCity' and i[2]!='Accttype']
    if len(li)>0:
        newdata.append((d[0],{'entities':li}))
# print(newdata)
with open("new_training_data","w") as f:
    json.dump(newdata,f)