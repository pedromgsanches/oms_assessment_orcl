# Description:
I made this customized assessment tool for Oracle Databases for a specific purpose and it may be useful for many similar others.
Execute SQL (1 col), write in SQLite3 database, output to JSON, XLSX, upload to Azure storage.

# Usage: #
Compiled software and example files in "./dist" folder.

## Generating Secrets File ##
- Use secrets.json.template to create a secrets.json file containing connect data
- Run secretsStore.exe to get help generating a salt key binary file and an encrypted file based on secrets.json file

## Getting data ##
- Use loads.json.template to create a loads.json file containing Queries metadata
- Save a secrets.json copy in a secret and safe place (Keepass file outside the server?)
- Run getData_orcl.exe to get Oracle data based on loads.json metadata and save it to a local SQLite3 database file

## Writing data to JSON ##
- Run outputJSON.exe to write data into JSON files

## Uploading data to Azure Storage ##
- TBA

## Writing data to XLSX ##
- TBA

# Dev Notes # 
**python modules:**
pip install pyinstaller, getopt, sys, cryptography, os, json, sqlite3, datetime, cx_Oracle, cryptography

**V_ENV activator:**
./scripts/activate.bat

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

- [ ] TO DO:
- **Load Azure**
- **Write XLSX**
- **Enrich loads.json -- adicionar SELECT's para trazer dados. O assessment em si.**
