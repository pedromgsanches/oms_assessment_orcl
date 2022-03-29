import os, uuid
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

connect_str = 'DefaultEndpointsProtocol=https;AccountName=cenas-exemplo;AccountKey=bananas;EndpointSuffix=core.windows.net'
local_path = "./output_JSON"
container_name = str('test-container')
exceptionsFile = "./uploadExceptions.log"

uploaded_path=local_path+"/uploaded/"
exceptfile = open(exceptionsFile, 'a')
exceptionCount=0

print('----------------- uploadAZURE -----------------')
try:
    os.mkdir(uploaded_path)
except Exception as er:
    None

try:
    print("Azure Blob Storage Driver v" + __version__ )
    print(" ")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.create_container(container_name)
except Exception as e:
    exceptionCount=exceptionCount+1
    exceptfile.write('\n----------------------------------------------------------------------------------------------------------------\n')
    exceptfile.write(str(e))

print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' - Uploading to Azure Storage as Blob:')

for filename in os.scandir(local_path):
    if filename.is_file():
        upload_file_path = filename.path
        local_file_name = filename.name
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
        with open(upload_file_path, "rb") as data:
            try:
                blob_client.upload_blob(data)
                print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" - "+ local_file_name)
                os.rename(filename.path, uploaded_path+filename.name)
            except Exception as e:
                exceptionCount=exceptionCount+1
                exceptfile.write('\n------------------------------------------------------------------------------------------------------------------\n')
                exceptfile.write(str(e))

if exceptionCount>0:
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' - '+str(exceptionCount)+' exception(s) found and described in '+exceptionsFile)
exceptfile.close()
print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' - Done.')

