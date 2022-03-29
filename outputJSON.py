import os, sqlite3, sys, getopt, json, re
from datetime import datetime

#sqliteAUX = "./database.db"
#Folder="./JSONoutput/"

################### OPTIONS/HELP MENU ####################
### SET VARS
sqliteAUX = None
Folder = None 

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



























## Open Files
sqliteCon = sqlite3.connect(sqliteAUX)
sqliteCurList = sqliteCon.cursor()
## Get Servers Data from SQLLite
try:
  sqliteCurList.execute("select distinct alias,host,port,database from raw_data")
except:
    print("SQLite error: "+str(e))
print("# outputJSON Starting... ")
Lmain=[]
Lconn=[]
for rowD in sqliteCurList.fetchall():
    Lconn=[ rowD[0],rowD[1],rowD[2],rowD[3]]
    Lmain.append(Lconn)
    #print(Lmain)
sqliteCurList.close()
dateNOW=datetime.now().strftime('%Y%m%d_%H%M')

# Get Data and write into Files
for value in Lmain:
    sqliteCur = sqliteCon.cursor()
    jsonOutput=str(Folder+re.sub(r'[^\w]', '_', value[0])+"_"+value[1]+"_"+value[2]+"_"+value[3]+"_"+dateNOW+".json")
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" - Writing: "+jsonOutput)
    outFile=open(jsonOutput, "a")

    try:
        sqliteCur.execute("select timestamp, alias, org, stage, label, host, port, database, \
            describe, additinfo, context, query_result, query_expected, equal, failure_msg \
                from raw_data where alias = ? and host = ? and port = ? and database = ?", (value[0], value[1], value[2], value[3]))
    except:
        print("SQLite error: "+str(e))
    
    itemsList=[]
    cnt=0
    outFile.write("[")
    for rowg in sqliteCur.fetchall():
        itemsDict = {
            "Date": rowg[0],
            "Alias": rowg[1],
            "Org": rowg[2],
            "Stage": rowg[3],
            "Label": rowg[4],
            "Host": rowg[5],
            "Port": rowg[6],
            "Database": rowg[7],
            "Describe": rowg[8],
            "AdditionalInfo": rowg[9],
            "Context": rowg[10],
            "QueryResult": rowg[11],
            "QueryExpected": rowg[12],
            "IsEqual": rowg[13],
            "FailureMsg": rowg[14]
            }
        jsonObject = json.dumps(itemsDict, indent = 2) 
        if cnt>0:
            outFile.write(","+jsonObject)
        else:
            outFile.write(jsonObject)
            cnt=cnt+1
            itemsList.append(jsonObject)
    outFile.write("]")
    outFile.close()

print("# outputJSON Done... ")
