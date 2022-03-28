import json

loadsFile="./loads.json"
saltFile="./saltFile"
connectionsFile="./secretsFile"
outputSQLITE="./database.db"
OracleHome="c:\instantclient"


################### HELP MENU #################



################# OPTIONS #####################


############ HELPER FUNCTIONS #################

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


############ MAIN FUNCTIONS ###################










## LOAD Loads File
# read file
with open(loadsFile, 'r') as loads_file:
    Loadsdata=loads_file.read()
LoadObj = json.loads(Loadsdata)

### HELPER LOAD GET CONFIG #########
for details in LoadObj['GETConfig']:
  print(str(details['Describe']))

# decrypt file



# show values
#print("usd: " + str(obj['usd']))
#print("eur: " + str(obj['eur']))
#print("gbp: " + str(obj['gbp']))

#with open('.\loads.json') as json_file:
#    data = json.load(json_file)
#    print(data)