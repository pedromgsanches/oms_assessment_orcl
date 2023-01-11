import csv, json


## INPUT
#"oms assessment db", "telepac", "development", "small7.1.4", "192.168.0.33", "1521", "SALESDB_DEV", "audit_user", "devpasssw0rd123asdc44##$#asdasdf"
#"oms assessment db", "telepac", "certification", "small7.1.4", "192.168.1.32", "1521", "SALESDB_CER", "audit_user", "cerpasssw0rd123asodiq098we09qid"
#"oms assessment db", "telepac", "production", "small7.1.4", "192.168.2.35", "1521", "SALESDB_PRD", "audit_user", "prdpasssw0rd123as9d8as98d23d"

## OUTPUT
# {"Databases": [
# { "Alias": "oms assessment database", "Org": "OramixManagedServices", "Stage": "development", "Label": "small_21c", "Host": "192.168.0.33", "Port": "1521", "Database": "ORCLCDB", "Username": "c##oramix", "Password": "batatas" }
# ] }

# read arguments add assign to variables
    # input csv file

file = open('csv_secrets.csv')
type(file)
csvreader = csv.reader(file)

header = []
header = next(csvreader)
header
header_length=range(len(header))

rows = {}
all_rows = []

dict_list = []
dict_dict = {}

for row in csvreader:
    print("----------------------------------------------------")
    diction = {}
    for head_idx in header_length:
        print(header[head_idx]+": "+row[head_idx].strip().replace("\"",""))
        diction[header[head_idx]] =  row[head_idx].strip().replace("\"","")
    print(diction)
    dict_list.append(diction)

print(dict_list)


#    for i in header_length:
        #head0 = row0
            #(...)
#        row_result = 
#    all_rows.append(row_result)

# final_doc = {databases: [row_result]}
 
 
#         rows.append(row)

file.close()

#print(header)

#print(rows)

#json.dumps()


# output file exists?

# test csv file

# convert CSV to JSON

# write data in output file

# bye 


