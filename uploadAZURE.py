import os, uuid, sys, getopt
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

connect_str = None
local_path = None 
container_name = None 
exceptionsFile = "./Exceptions.log"
exceptfile = open(exceptionsFile, 'a')
exceptionCount=0
runUploadData=False

################### OPTIONS/HELP MENU ####################
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "ho:d:o,r"
long_options = ["help", "database=", "outputDest=", "run"]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
# Output error, and return with an error code
    print (str(err))
    sys.exit(2)

def display_help():
    print('--- OutputJSON help ----------------------------------------------------------------------------------------------------')
    print(' ')
    print('  -h, --help  Display Help')
    print('  -s, --stringconn= Azure Blob Storage connect string \n')
    print('  -c, --container= Azure Blob Storage container name \n')
    print('  -l, --localpath= Local path where to be uploaded files live\n')
    print('  -r, --run  Run this tool.')
    print(' ')
    print('Example Usage: ---------------------------------------------------------------------------------------------------------')    
    print('- outputJSON.exe -c "bikeStore_dbAssessment" -l "./upload_JSON_bikeStore" -s DefaultEndpointsProtocol=https;AccountName=My_DB_Assessments;AccountKey=bananas123;EndpointSuffix=core.windows.net  ')
    print(' ')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------------------------')
    sys.exit()

##################################################### DEFINE VARS ###########################################################################################

# No Arguments? Return HELP!
try:
    sys.argv[1]
except IndexError as ie:
    display_help()
# Evaluate given options
for current_argument, current_value in arguments:
    if current_argument in ("-h", "--help"):
        display_help()
    elif current_argument in ("-s", "--strinconn"):
        print (("Azure Storage connect string= (%s)") % (current_value))
        connect_str=current_value
    elif current_argument in ("-c", "--container"):
        print (("Azure Storage Container= (%s)") % (current_value))
        container_name=current_value
    elif current_argument in ("-l", "--localpath"):
        print (("Data local path= (%s)") % (current_value))
        local_path = current_value
        uploaded_path = local_path+"/uploaded/"

    elif current_argument in ("-r", "--run"):
        print('Executing... ')
        runUploadData=True

################# OPTIONS DEFINITION #####################
if connect_str is None:
    print('Please provide a valid Azure Storage Connect String \n \
        More info in the following link: \n \
        - https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=environment-variable-windows \n')
    sys.exit()
if container_name is None:
    print('Please provide a Azure Storage Container \n')
    sys.exit()
if local_path is None:
    print('Please provide a local path \n')
    sys.exit()


### MAIN ACTION ######################################################
def uploadAzureData():
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
                   ## devia mover, mas ainda nao o está a fazer
                    os.rename(filename.path, str(uploaded_path+filename.name))
                except Exception as e:
                    exceptionCount=exceptionCount+1
                    exceptfile.write('\n------------------------------------------------------------------------------------------------------------------\n')
                    exceptfile.write(str(e))

    if exceptionCount>0:
        print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' - '+str(exceptionCount)+' exception(s) found and described in '+exceptionsFile)
    exceptfile.close()
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' - Done.')



if runUploadData is True:
    uploadAzureData()

