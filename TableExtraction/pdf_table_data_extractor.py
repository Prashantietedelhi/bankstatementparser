from tabula import wrapper
import os
print(os.listdir("."))
filepath=r"Birddogs-BofA-Bank-Statement-April.'17.pdf"

tables = wrapper.read_pdf(filepath,
                       pages='all',
                       silent=True,
                       pandas_options={
                           'header': None,
                           'error_bad_lines': False,
                           'warn_bad_lines': False
                       })
# tables = wrapper.read_pdf(filepath,multiple_tables=True,pages='all')

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
for r in (tables.values.tolist()):
    print(r)
# for table in tables:
#     table.to_excel(os.path.join(folder,'Results'+str(i)+'.xlsx'),index=False)
#     print(i)
#     i=i+1

