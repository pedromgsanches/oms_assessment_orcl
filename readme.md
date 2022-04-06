# Description:
Customized assessment tool for Oracle Databases. \
Main purposes:
- Execute SQL (1 col), 
- write in SQLite3 database, 
- output to JSON, XLSX, etc
- upload to cloud storage (Azure, etc)

# Usage: #
Compiled software and example files in "./dist" folder.

## Generating Secrets File ##
- Use secrets.json.template to create a secrets.json file containing connect data
- Run secretsStore exec file to get help generating a salt key binary file and an encrypted file based on secrets.json file
**- If needed, it's possible to create one secrets-file per organization or context. ex: "secrets-cocacola-prd, secrets-cocacola-dev, secrets-vitoriafc-dev"**

## Getting data ##
- Use loads.json.template to create a loads.json file containing Queries metadata
- Save a secrets.json copy in a secret and safe place (Keepass file outside the server?)
- Run getData_orcl exec file to get Oracle data based on loads.json metadata and save it to a local SQLite3 database file
**- It's recommended to create one loads file per load context. Ex: "SVC-ORCL-BCKP-ASSESSMENT.json"**

## Writing data to JSON ##
- Run outputJSON exec file to write data into JSON files
**- It's recommended to output data to a folder with the same name as loads.json file. Ex: For SVC-ORCL-ASSESSMENT.json, use ./SVC-ORCL-ASSESSMENT/"

## Uploading data to Azure Storage ## -- not working in Linux, yet.
- Run uploadAZURE exec file to upload data into Azure Blob Storage
**- Source folder, with the same name as loads.json file, Ex: "./SVC-ORCL-BCKP-ASSESSMENT/", will be created in Azure Blob Container**


## Writing data to XLSX ##
- TBA

# Dev Notes # 
**python modules:**
pip install pyinstaller, getopt, sys, cryptography, os, json, sqlite3, datetime, cx_Oracle, cryptography

**V_ENV activator:**
- Windows: ./scripts/activate.bat
- Gnu/Linux: 
   - . ./scripts/activate
   - export LD_LIBRARY_PATH=<ORACLE_CLIENT_HOME>

**Build EXE files:**
./build.bat


- [x] DONE
- **Tool encrypt/decrypt JSONs - secretStore.exe**
- **Connections encrypted JSON file**
- **Loads JSON file**
- **Get Oracle Data (getData_orcl.exe)**
- **Write data to SQLite3 (database.db)**
- **Write JSON** \
   Output (sample):
    { \
        "Date":  "02/22/22 14:59:55", \
        "Label":  "Produção", \
        "Describe":  "Agent Alerts", \
        "Context":  "Testing Agent Alerts Severity exists", \
        "Name":  "Severity 25 Alert should have a notification", \
        "Database":  null, \
        "ComputerName":  "server.app.ROOT", \
        "Instance":  "server.app.ROOT\\DB001", \
        "Result":  "Failed", \
        "FailureMessage":  "Expected $true, because Should notify by Agent notifications, but got $false." \
     }, \
\
- **Load Azure** -- uploadAZURE.py  

- [ ] IN PROGRESS:
- Melhorias **Load Azure** -- uploadAZURE.py:
   - [x] ainda nao move para "uploaded"
   - [x] validar em storage em uso
   - [ ] correr em Gnu/Linux


- [ ] TO DO:
- **Write XLSX**
- **Enrich loads.json -- adicionar SELECT's para trazer dados. O assessment em si.**
