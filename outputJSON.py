import os, sqlite3, sys, getopt, json, re
from datetime import datetime

#sqliteAUX = "./database.db"
#Folder="./output_JSON/"

################### OPTIONS/HELP MENU ####################
### SET VARS
sqliteAUX = None
Folder = None 
runWRITEdata = False

#### Command Line Options ################################################################################3
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
    print('### OMS #################################################################################################################')
    print('--- OutputJSON help -----------------------------------------------------------------------------------------------------')
    print(' ')
    print('  -h, --help  Display Help')
    print('  -d, --database= auxiliary SQLite3 database. \n \
            Default file: ./database.db')
    print('  -o, --outputDest= Output destination for JSON files. \n \
            Default location: "./output_JSON/"')
    print('  -r, --run  Run this tool.')
    print(' ')
    print('Example Usage: ---------------------------------------------------------------------------------------------------------')    
    print('- outputJSON -d ./database.db -o "./output_JSON/" -r ')
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
    elif current_argument in ("-d", "--database"):
        print (("Custom Database File= (%s)") % (current_value))
        sqliteAUX=current_value
    elif current_argument in ("-o", "--outputDest"):
        print (("Custom JSON output destination= (%s)") % (current_value))
        Folder=current_value
    elif current_argument in ("-r", "--run"):
        print('Executing... ')
        runWRITEdata=True

################# OPTIONS DEFINITION #####################
if sqliteAUX is None:
    sqliteAUX="./database.db"
    print('Using default database file='+sqliteAUX)
if Folder is None:
    Folder="./output_JSON/"
    print('Using default output destination='+Folder)



def outputJSON():
    ## Open Files
    sqliteCon = sqlite3.connect(sqliteAUX)
    sqliteCurList = sqliteCon.cursor()
    ## Get Servers Data from SQLLite
    try:
        sqliteCurList.execute("select distinct alias,host,port,database,org from raw_data")
    except:
        print("SQLite error: "+str(e))
    print("# outputJSON Starting... ")
    Lmain=[]
    Lconn=[]
    for rowD in sqliteCurList.fetchall():
        Lconn=[ rowD[0],rowD[1],rowD[2],rowD[3],rowD[4] ]
        Lmain.append(Lconn)
        #print(Lmain)
    sqliteCurList.close()
    dateNOW=datetime.now().strftime('%Y%m%d_%H%M')
    # Get Data and write into Files
    for value in Lmain:
        sqliteCur = sqliteCon.cursor()

        if os.path.isdir(Folder) is False:
            os.mkdir(Folder)
        
        if os.path.isdir(Folder+re.sub(r'[^\w]', '_', value[4])) is False:
            os.mkdir(Folder+re.sub(r'[^\w]', '_', value[4]))

        jsonOutput=str(Folder + re.sub(r'[^\w]', '_', value[4]) + '/' +re.sub(r'[^\w]', '_', value[0])+"_"+value[1]+"_"+value[2]+"_"+value[3]+"_"+dateNOW+".json")
        outFile=open(jsonOutput, "a")

        print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+" - Writing: "+jsonOutput)
        try:
            sqliteCur.execute("select timestamp, alias, org, stage, label, host, port, database, \
                describe, additinfo, context, query_result, compare_op, query_expected, equal, failure_msg \
                from raw_data where alias = ? and host = ? and port = ? and database = ?", (value[0], value[1], value[2], value[3]))
        except Exception as e:
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
                "CompareOperator": rowg[12],
                "QueryExpected": rowg[13],
                "IsCompliant": rowg[14],
                "FailureMsg": rowg[15]
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

if runWRITEdata is True:
    outputJSON()
