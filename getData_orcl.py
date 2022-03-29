import sys, json, cx_Oracle, sqlite3, getopt
from cryptography.fernet import Fernet
from datetime import datetime

#loadsFile="./loads.json"
#saltFile="./saltFile"
#ConnectionsFile="./secretsFile"
#oSqlite="./database.db"
#OracleHome="c:\instantclient"

################### OPTIONS/HELP MENU ####################
saltFile = None
loadsFile = None
ConnectionsFile = None
oSqlite = None
OracleHome = None

#### Command Line Options ################################################################################3
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "ho:s:l:c:d,o,r"
long_options = ["help", "saltFile=", "loadsFile=", "connectionsFile=" , "database=", "OracleHome=", "run"]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
# Output error, and return with an error code
    print (str(err))
    sys.exit(2)

def display_help():
    print('--- Get ORCL Data help ----------------------------------------------------------------------------------------------------')
    print(' ')
    print('  -h, --help  Display Help')
    print('  -s, --saltFile= SaltFile Location for connectionsFile Decrypt \n \
            Default: ./saltFile')
    print('  -c, --connectionsFile= secrets connections file created under secretStore.exe file. \n \
            Default file: secretsFile')
    print('  -l, --loadsFile= for execution info metadata. Please follow the example in loads.json.example \n \
            Default file: ./loads.json')
    print('  -d, --database= auxiliary SQLite3 database. \n \
            Default file: ./database.db')
    print('  -o, --OracleHome= ORACLE_HOME location. \n \
            Default location: ORACLE_HOME=c:\instantclient')
    print('  -r, --run  Run this tool.')
    print(' ')
    print('Example Usage: ---------------------------------------------------------------------------------------------------------')    
    print('- getData_orcl.exe -s ./saltFile -c secretsFile_dev -l loads_dev.json -o c:\oracle\home\ -r ')
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

    elif current_argument in ("-s", "--saltFile"):
        print (("Custom salt File= (%s)") % (current_value))
        saltFile=current_value

    elif current_argument in ("-c", "--connectionsFile"):
        print (("Custom Connections File= (%s)") % (current_value))
        ConnectionsFile=current_value

    elif current_argument in ("-l", "--loadsFile"):
        print (("Custom Loads File= (%s)") % (current_value))
        loadsFile=current_value

    elif current_argument in ("-d", "--database"):
        print (("Custom SQLite3 Database File= (%s)") % (current_value))
        oSqlite=current_value

    elif current_argument in ("-o", "--OracleHome"):
        print (("Custom client ORACLE_HOME= (%s)") % (current_value))
        OracleHome=current_value

    elif current_argument in ("-r", "--run"):
        print('Executing... ')
        runGETdata=True


################# OPTIONS DEFINITION #####################
if saltFile is None:
    saltFile="./saltFile"
    print('Using default Salt File='+saltFile)
if ConnectionsFile is None:
    ConnectionsFile="./secretsFile"
    print('Using default Connections File='+ConnectionsFile)
if loadsFile is None:
    loadsFile="./loads.json"
    print('Using default LoadsFile='+loadsFile)
if oSqlite is None:
    oSqlite="./database.db"
    print('Using default SQLite3 Database='+oSqlite)
if OracleHome is None:
    OracleHome="c:\instantclient"
    print('Using default client ORACLE_HOME='+OracleHome)


############ HELPER FUNCTIONS #################
#### Function Read Salt File --- used on above functions 
def openSalt(saltFile):
    with open (saltFile,'r') as Sfile:
        key = Sfile.read()
    Sfile.close()
    #print("BinaryKey: "+str(key))
    fernet = Fernet(key)
    return(fernet)

#### GET ORACLE CONN DATA ######################
def getConnData(saltF,ConnF):
    ffernet=openSalt(saltF)
    with open (ConnF,'rb') as Kfile:
        encData = Kfile.read()
    decData = ffernet.decrypt(encData).decode()
    return(decData)

#### IF FILE EXISTS ############################
def testFiles(testFile):
    tfile = exists(testFile)
    return(tfile)

#### YES OR NO? ################################
def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

#### GET LOADS ################################
def GetLoads(loadsFile):
  with open(loadsFile,'r') as LoFile:
    try:
      LoData=json.loads(LoFile.read())
    except Exception as e:
      print('ERR: Validate your Loads JSON file: '+str(e))
      sys.exit()
    return(LoData['metaGetData'])

def OrclGet(host,port,user,password,query):
  x = 1
  return(x)

#### INIT SQLITE ################################
def InitSQLite3(SQLITE):
  sqliteCon = sqlite3.connect(SQLITE)
  sqliteCur = sqliteCon.cursor()
  try:
    sqliteCur.execute('''DROP TABLE raw_data''')
    sqliteCon.commit()
  except Exception as e: 
    print('SQLITEerr: '+str(e))
  try:
    sqliteCur.execute('''CREATE TABLE raw_data (timestamp, alias, org, stage, label, host, port, database, describe, additinfo, context, query_result,query_expected,equal,failure_msg)''')
    sqliteCon.commit()
  except Exception as e: 
    print('SQLITEerr: '+str(e))
  sqliteCon.close()


############ MAIN FUNCTIONS #############################################################################
def getOrclData(saltFile,ConnectionsFile):
  cx_Oracle.init_oracle_client(lib_dir=OracleHome)
  #for connData in getConnData(saltFile,ConnectionsFile):
 #   json.loads(connData)
  jsonData = getConnData(saltFile,ConnectionsFile)
    #print(jsonData)
  InitSQLite3(oSqlite)
  sqliteCon = sqlite3.connect(oSqlite)
  sqliteCur = sqliteCon.cursor()

  print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' - Starting...')

  
  try:
    conData = json.loads(jsonData)
  except Exception as e:
    print('ERR: Validate your JSON in secrets file: '+str(e))
    sys.exit()
  #print(str(conData['Databases']))
  for db in conData['Databases']:
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' - Connecting: ['+ db["Alias"] +"] "+db["Host"]+":"+db["Port"]+"/"+db["Database"])
    connection = cx_Oracle.connect(user=db["Username"], password=db["Password"],dsn=db["Host"]+":"+db["Port"]+"/"+db["Database"])
    for loadar in GetLoads(loadsFile):    
      cursor = connection.cursor()
      cursor.execute(loadar["Query"])
      for LQuery in cursor:
        if str(LQuery[0]) == str(loadar["ExpectedValue"]):
          isEqual = 'OK'
        else:
          isEqual = 'NOT_OK'
        
        print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" - "+loadar['Describe'])
        sqliteCur.execute("insert into raw_data values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
        (datetime.now(),db['Alias'], db['Org'], db['Stage'], db['Label'], db['Host'], db['Port'], db['Database'], loadar['Describe'], loadar['AdditInfo'],loadar['Context'], str(LQuery[0]),loadar["ExpectedValue"],isEqual,loadar["FailureMessage"]))
        sqliteCon.commit()
        #print(row)
  sqliteCur.close()
  sqliteCon.close()

print("-------------------------------------------------------")


if runGETdata is True:
  print(getOrclData(saltFile,ConnectionsFile))




# print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" - Starting..")

####### LOAD Loads File ########################
# read file
#with open(loadsFile, 'r') as loads_file:
#    Loadsdata=loads_file.read()
#LoadObj = json.loads(Loadsdata)

### HELPER LOAD GET CONFIG #########
#for details in LoadObj['GETConfig']:
#  print(str(details['Describe']))






# decrypt file






