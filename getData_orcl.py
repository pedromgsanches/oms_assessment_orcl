import sys, json, cx_Oracle
from cryptography.fernet import Fernet

loadsFile="./loads.json"
saltFile="./saltFile"
ConnectionsFile="./secretsFile"
oSqlite="./database.db"
OracleHome="c:\instantclient"

cx_Oracle.init_oracle_client(lib_dir=OracleHome)


################### OPTIONS/HELP MENU ####################



################# OPTIONS DEFINITION #####################


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
    print('SQLITEerr: '+str(e)
  try:
    sqliteCur.execute('''CREATE TABLE raw_data (timestamp, alias, org, stage, label, host, port, database, describe, additinfo, context, query_result,query_expected,failure_msg)''')
    sqliteCon.commit()
  except Exception as e: 
    print('SQLITEerr: '+str(e))


############ MAIN FUNCTIONS #############################################################################
def getOrclData(saltFile,ConnectionsFile):
  #for connData in getConnData(saltFile,ConnectionsFile):
 #   json.loads(connData)
  
  jsonData = getConnData(saltFile,ConnectionsFile)
  #print(jsonData)
  try:
    conData = json.loads(jsonData)
  except Exception as e:
    print('ERR: Validate your JSON in secrets file: '+str(e))
    sys.exit()
  #print(str(conData['Databases']))

  for db in conData['Databases']:
    print(db["Host"]+" "+db["Port"]+" "+db["Database"] +" "+db["Username"]+" "+db["Password"])
    for loadar in GetLoads(loadsFile):
      if loadar["Query"] is not None:
        print("X-"+" "+loadar["Query"])




#print(GetLoads(loadsFile))
#for i in GetLoads(loadsFile):
#  print(i['Label'])

print("-------------------------------------------------------")
print(getOrclData(saltFile,ConnectionsFile))




# print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" - Starting..")
# InitSQLite3(oSqlite)

####### LOAD Loads File ########################
# read file
#with open(loadsFile, 'r') as loads_file:
#    Loadsdata=loads_file.read()
#LoadObj = json.loads(Loadsdata)

### HELPER LOAD GET CONFIG #########
#for details in LoadObj['GETConfig']:
#  print(str(details['Describe']))






# decrypt file






