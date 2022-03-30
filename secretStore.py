import getopt, sys
from multiprocessing.pool import RUN
from operator import truediv
from cryptography.fernet import Fernet
from os.path import exists

##### INIT PARAMS ###################################
saltFile = None
inputFile = None
outputFile = None
generateSalt = None
createSecrets = None
printSecrets = None

#### Command Line Options ################################################################################3
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "ho:s:i:o:po:ro:go"
long_options = ["help", "saltFile=", "input=", "output=" , "print", "run", "genSalt"]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
# Output error, and return with an error code
    print (str(err))
    sys.exit(2)

def display_help():
    print('### OMS #################################################################################################################')
    print('--- SecretStore help ----------------------------------------------------------------------------------------------------')
    print(' ')
    print('  -h, --help  Display Help')
    print('  -s, --saltFile= Location \n \
            Default: ./saltFile')
    print('  -i, --input= file in JSON format. Please follow secrets.json.example \n \
            Default file: secrets.json')
    print('  -o, --output= file in Binary format. \n \
            Default file: secretsFile')
    print('  -p, --print secrets in output file. \n \
            Default file: secretsFile')
    print('  -r, --run  Run secretsFile generation with default options.')
    print('  -g, --genSalt  Generate SaltFile.')
    print(' ')
    print('Example Usage: ---------------------------------------------------------------------------------------------------------')    
    print('- generate Salt File:      ./secretStore.exe -g -s "saltFile" ')
    print('- create secrets file:     ./secretStore.exe -r -s "saltFile" -i "secrets.json" -o "secretsFile" ')
    print('- print secrets:           ./secretStore.exe -p -s "saltFile" -o "secretsFile" ')
    print(' ')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('--- ATENTION! ----------------------------------------------------------------------------------------------------------')
    print('PLEASE SAVE SECRETS (secrets.json) IN A SAFE PLACE AFTER CREATING SECRETS FILE (secretsFile) , IT HAVE PASSWORDS IN IT.')
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

    elif current_argument in ("-s", "--saltFile"):
        print (("Custom salt file= (%s)") % (current_value))
        saltFile=current_value

    elif current_argument in ("-i", "--input"):
        print (("Custom Input file= (%s)") % (current_value))
        inputFile=current_value

    elif current_argument in ("-o", "--output"):
        print (("Custom Output file= (%s)") % (current_value))
        outputFile=current_value

    elif current_argument in ("-p", "--print"):
        print('Print Secrets')
        printSecrets=True

    elif current_argument in ("-r", "--run"):
        print('Generating secrets file... ')
        createSecrets=True
        
    elif current_argument in ("-g", "--genSalt"):
        print('Generating salt file with default option')
        generateSalt=True

if saltFile is None:
    saltFile="./saltFile"
    print('Using default SaltFile='+saltFile)
if inputFile is None:
    inputFile="./secrets.json"
    print('Using default Input='+inputFile)
if outputFile is None:
    outputFile="./secretsFile"
    print('Using default Output='+outputFile)

print('------------------------------------------------------')

#### HELPER FUNCTIONS #################################################################
#### Function Read Salt File --- used on above functions #####################
def openSalt(saltFile):
    with open (saltFile,'r') as Sfile:
        key = Sfile.read()
    Sfile.close()
    #print("BinaryKey: "+str(key))
    fernet = Fernet(key)
    return(fernet)
    
def testFiles(testFile):
    tfile = exists(testFile)
    return(tfile)

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False


####### MAIN FUNCTIONS #########################################################################

#### Option Gen Salt File ##################################################
def genSalt(saltFile):
    key = Fernet.generate_key()
    print("## Generated Key: "+str(key)+" in file: "+saltFile+". Please keep it in a safe place.")
    f = open(saltFile, "wb")
    f.write(key)
    f.close()



#### Option Crypt Connections File ###########################################
def enCryptFile(saltFile,inputFile,outputFile):
    ffernet=openSalt(saltFile)

    with open(inputFile, 'r') as loads_file:
        message=loads_file.read()

    encMessage = ffernet.encrypt(message.encode())
    c = open(outputFile,'wb')
    c.write(encMessage)
    c.close()
    print('Created secrets file: '+outputFile)

#### Option Decrypt Connections File #########################################
def deCryptFile(saltFile,outputFile):
    ffernet=openSalt(saltFile)
    with open (outputFile,'rb') as Kfile:
        encMessage = Kfile.read()
    decMessage = ffernet.decrypt(encMessage).decode()
    return(decMessage)


### IF OPTION, EXECUTE ######################################################
if generateSalt is True:
    if testFiles(saltFile) is True:
        if yes_or_no("SaltFile exists. Replace?") is True:
            genSalt(saltFile)
        else:
            print('Bye!')
            sys.exit()
    else:
        genSalt(saltFile)
        sys.exit()

if printSecrets is True:
    if testFiles(saltFile) is True:
      if testFiles(outputFile) is True:
        print('## Decrypted secrets: ')
        print(deCryptFile(saltFile,outputFile))
      else:
        print('ERR: Output file "'+outputFile+'" is missing.')
    else: 
      print('ERR: salt file "'+saltFile+'" is missing')
    

if createSecrets is True:    
    if testFiles(inputFile) is not True:
        sys.exit()
    if testFiles(outputFile) is True:
        if yes_or_no("Output exists. Replace?") is False:
            print('Bye!')
            sys.exit()
    if testFiles(saltFile) is not True:
        genSalt(saltFile)
    enCryptFile(saltFile,inputFile,outputFile)

###### EOF ##########################################################