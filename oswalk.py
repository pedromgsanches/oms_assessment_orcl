import os


Folder='.\output_JSON'

for root,dirs,files in os.walk(Folder):
    for file in files:
        file_name=os.path.join(root, file)
        #print(fileName)
        filename=file_name[file_name.startswith(Folder) and len(Folder)+1:]
        print(filename)


