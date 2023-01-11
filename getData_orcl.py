from ast import operator
import sys, json, cx_Oracle, sqlite3, getopt, os, re
from cryptography.fernet import Fernet
from datetime import datetime

################### OPTIONS/HELP MENU ####################
saltFile = None
loadsFile = None
ConnectionsFile = None
oSqlite = None
OracleHome = None

#### Command Line Options ################################################################################3
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "ho:s:q:c:d:o,r"
long_options = ["help", "saltFile=", "queries=", "connectionsFile=" , "database=", "OracleHome=", "run"]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
# Output error, and return with an error code
    print (str(err))
    sys.exit(2)

def display_help():
    print('### OMS #################################################################################################################')
    print('--- Get ORCL Data help --------------------------------------------------------------------------------------------------')
    print(' ')
    print('  -h, --help  Display Help')
    print('  -s, --saltFile= SaltFile Location for connectionsFile Decrypt \n \
            Default: ./saltFile')
    print('  -c, --connectionsFile= secrets connections file created under secretStore file. \n \
            Default file: secretsFile.conn')
    print('  -q, --queries= for execution info metadata. Please follow the example in queries.json.example \n \
            Default file: ./queries.json')
    print('  -d, --database= auxiliary SQLite3 database. \n \
            Default file: ./database.db')
    print('  -o, --OracleHome= ORACLE_HOME location. \n \
            Default location: LD_LIBRARY_PATH=c:\instantclient')
    print('  -r, --run  Run this tool.')
    print(' ')
    print('Example Usage: ---------------------------------------------------------------------------------------------------------')    
    print('- getData_orcl -s ./saltFile -c my_company_secrets.conn -q my_assessment_queries.json -o c:\oracle\home\ -r ')
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

runGETdata=False

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

    elif current_argument in ("-q", "--queries"):
        print (("Custom Queries File= (%s)") % (current_value))
        loadsFile=current_value

    elif current_argument in ("-d", "--database"):
        print (("Custom SQLite3 Database File= (%s)") % (current_value))
        oSqlite=current_value

    elif current_argument in ("-o", "--OracleHome"):
        print (("Custom client ORACLE_HOME= (%s)") % (current_value))
        OracleHome=current_value
        os.environ["LD_LIBRARY_PATH"] = OracleHome
        print('Using ORACLE_HOME='+OracleHome)
        print(os.environ["LD_LIBRARY_PATH"])

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
    loadsFile="./queries.json"
    print('Using default Queries File='+loadsFile)
if oSqlite is None:
    oSqlite="./database.db"
    print('Using default SQLite3 Database='+oSqlite)
if OracleHome is None:
    OracleHome="c:\instantclient"
    os.environ["LD_LIBRARY_PATH"] = OracleHome
    print('Using default client ORACLE_HOME='+OracleHome)
    print(os.environ["LD_LIBRARY_PATH"])

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

#### COMPARE VALUES ###########################
def compareValues(GotValue, ExpecValue, inputOp):
  outputValue=False

  if inputOp == 'equal':
      if GotValue == ExpecValue:
        outputValue = True
  if inputOp == 'greater':
      if GotValue > ExpecValue:
        outputValue = True
  if inputOp == 'less':
      if GotValue < ExpecValue:
        outputValue = True
  if inputOp == 'or':
      match = re.findall(re.escape(GotValue), ExpecValue)
      if match:
        outputValue = True
  return(outputValue)

#### GET LOADS ################################
def GetLoads(loadsFile):
  with open(loadsFile,'r') as LoFile:
    try:
      LoData=json.loads(LoFile.read())
    except Exception as e:
      print('ERR: Validate your Queries JSON file: '+str(e))
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
    sqliteCur.execute('''CREATE TABLE raw_data (timestamp, alias, org, stage, label, host, port, database, describe, additinfo, context, query_result,compare_op,query_expected,equal,failure_msg,fail_msg)''')
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
    try:
      connection = cx_Oracle.connect(user=db["Username"], password=db["Password"],dsn=db["Host"]+":"+db["Port"]+"/"+db["Database"])
      for loadar in GetLoads(loadsFile):    
        cursor = connection.cursor()
        try:
          cursor.execute(loadar["Query"])
        except Exception as e:
          print('ERR: Something went wrong executing query: '+str(e))
        for LQuery in cursor:
          if compareValues(str(LQuery[0]),str(loadar["ExpectedValue"]),str(loadar["ExpectedValOperator"])) is True:
#          if str(LQuery[0]) == str(loadar["ExpectedValue"]):
            isEqual = 'OK'
          else:
            isEqual = 'NOT_OK'
        
          print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" - "+loadar['Describe'])
          sqliteCur.execute("insert into raw_data values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
          (datetime.now(),db['Alias'], db['Org'], db['Stage'], db['Label'], db['Host'], db['Port'], db['Database'], loadar['Describe'], loadar['AdditInfo'],loadar['Context'], str(LQuery[0]),loadar["ExpectedValOperator"],loadar["ExpectedValue"],isEqual,loadar["FailureMessage"],str(LQuery[1])))
          sqliteCon.commit()
          #print(row)
    except Exception as e:
      print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+'ERR: connecting: '+str(e))

  sqliteCur.close()
  sqliteCon.close()

print("-------------------------------------------------------")


if runGETdata is True:
  print(getOrclData(saltFile,ConnectionsFile))
else:
  display_help()



