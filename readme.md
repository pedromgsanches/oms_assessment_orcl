python modules:
pip install pyinstaller, getopt, sys, cryptography, os, json




DONE:
## Tool encrypt/decrypt JSONs:
## Connections encrypted JSON:
	{ 
		"Alias": "sonae prd database",
		"Label": "Produção",
		"hostname": "lx-app-db-01",
		"port": "1521",
		"username": "omixms",
		"password": "as89d0as90d"
	},
## Loads JSON:
    {
        "Describe":  "Agent Alerts",
        "Context":  "Testing Agent Alerts Severity exists",
        "Name":  "Severity 25 Alert should have a notification",
        "Query":  " select xcps from xpto"
        "ExpectedValue":  "abc",
        "FailureMessage":  "Expected $true, because Should notify by Agent notifications, but got $false."
    },
## Read Loads



TO DO:
## Read Connections/Decrypt on getData
## Execute connections
## Write SQLite
## Write XLSX
## Write JSON
   Output (sample):
    {
        "Date":  "02/22/22 14:59:55",
        "Label":  "Produção",
        "Describe":  "Agent Alerts",
        "Context":  "Testing Agent Alerts Severity exists",
        "Name":  "Severity 25 Alert should have a notification",
        "Database":  null,
        "ComputerName":  "SRVASCDBG1.GCA.AD.ROOT",
        "Instance":  "SRVASCDBG1.GCA.AD.ROOT\\DBG1",
        "Result":  "Failed",
        "FailureMessage":  "Expected $true, because Should notify by Agent notifications, but got $false."
     },

## Load Azure