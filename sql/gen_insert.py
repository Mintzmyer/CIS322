# Credit to stackoverflow for python syntax
import os.path
import psycopg

files = os.listdir(os.path.expanduser('~')+'/osnap_legacy')
for file in files:
    parseFile(file)

def lostQuery(sqlQuery):
    conn = psycopg.conn("lost")
    cur = conn.cursor()
    result = cur.exec(sqlQuery)
    return result
           # "SELECT user_id from users where ... INSERT INTO assets")


# Create order...spec doc order probably a good place to start
# Import File
def parseFile(csvFile):
    legacy = csvFile.split('.csv')[0]

    with open(csvFile) as table:
        lines = table.readlines()
#        lines = [x.strip() for x in lines]
    columns = lines[0]
    columns = columns.split(',')
    for line in lines:
        line = line.split(',')

    tables = updateTables(legacy)
    if legacy == "product_list":
        produtsInsert(legacy, lines)
    if (legacy == "DC_inventory") or (legacy == "HQ_inventory"):
        assetsInsert(legacy, lines)


def productsInsert(legacy, lines):
    #Check product is not already inserted
    #Insert Product/Check return success
def assetsInsert(legacy, lines):
    #Check asset is not already inserted
    #Insert asset/Check return success
def updateTables(legacy):
#Tables: 0-products, 1-assets, 2-vehicles, 3-facilities, 4-asset_at, 5-convoys, 6-used_by, 7-asset_on, 8-users, 9-roles, 10-user_is, 11-user_supports, 12-levels, 13-compartments, 14-security_tags
    return {
        'acquisitions': [],
        'convoy':       [],
        'DC_inventory': [],
        'HQ_inventory': [],
        'MB005_inventory': [],
        'NC_inventory': [],
        'product_list': [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
        'README':       [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
        'security_compartments': [],
        'security_levels': [],
        'SPNV_inventory': [],
        'transit'       : [],
        'vendors'       : [],
    }[legacy]

# Parse lines
# Grab elements of array line to generate sql statements
# Print SQL statement to insert.sql

#select column_name from information_schema.columns where table_name='assets';
