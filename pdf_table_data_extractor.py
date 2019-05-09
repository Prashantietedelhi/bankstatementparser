from tabula import wrapper
import os
filepath=r""
tables = wrapper.read_pdf(filepath,multiple_tables=True,pages='all')

folder = "results"
if os.path.isdir(folder) == False:
    os.makedirs(folder)
i=1

for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

for table in tables:
    table.to_excel(os.path.join(folder,'Results'+str(i)+'.xlsx'),index=False)
    print(i)
    i=i+1

