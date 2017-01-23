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
    for line in lines:
        line = line.split(',')

    tables = updateTables(legacy)
    callInsert(tables, legacy, lines)



def productsInsert(lines):
    #Find relevant data
    for i in range(len(lines[0])):
        if lines[0][i] == 'vendor': vendor = i
        if lines[0][i] == 'name': name = i
    #Check product is not already inserted
    for line in lines[1:]:
        preexisting = "SELECT product_pk from products where vendor='"+line[vendor]+"' and description='"+line[name]"';"
        exists = lostQuery(preexisting)
        #Insert Product/Check return success
        if not (exists):
            altdesc = ""
            for i in range(len(line)):
                if (i != vendor) and (i != name):
                    altdesc = altdesc + line[i]+", "
            insertNew = "INSERT INTO products(vendor,description,alt_description) VALUES ('"+line[vendor]+"', '"+line[desc]+"', '"+altdesc+"');"
            inserted = lostQuery(insertNew)
            if not (inserted): print("Error, "+line+" not inserted into products")
        else: print("Product "+line+" already exists in products")

def assetsInsert(lines):
    #Find relevant data
    for i in range(len(lines[0])):
        if lines[0][i] == 'asset tag': tag = i
        if lines[0][i] == 'description': desc = i
        if lines[0][i] == 'product': prod = i
    #Check asset is not already inserted
    for line in lines[1:]:
        productQ = "SELECT product_pk from products where description='"+line[prod]+"';"
        product_fk = lostQuery(productQ)
        if not (product_fk):
            insertNew = "INSERT INTO products(description) VALUES ('"+line[prod]+");"
        product_fk = lostQuery(productQ)
        preexisting = "SELECT asset_pk from assets where asset_tag='"+line[tag]+"';"
        exists = lostQuery(preexisting)
        #Insert asset/Check return success
        if not (exists):
            altdesc = ""
            for i in range(len(line)):
                if (i != tag) and (i != desc):
                    altdesc = altdesc + line[i]+", "
            insertNew = "INSERT INTO assets(product_fk, asset_tag, description, alt_description) VALUES ('"+product_fk+"', '"+line[asset]+"', '"+line[desc]+"', '"+altdesc+"');"
            inserted = lostQuery(insertNew)
            if not (inserted): print("Error, "+line+" not inserted into assets")
        else: print("Asset "+line+" already exists in assets")

def vehiclesInsert(lines):
    #Find relevant data
    for i in range(len(lines[0])):
        if lines[0][i] == 'assigned vehicles': vehicles = i
    #Check vehicle is not already inserted
    for line in lines[1:]:
        line[vehicles]= line[vehicles].split(',')
        for vehicle in line[vehicles]:
            preexisting = "SELECT product_pk from products where description='Convoy vehicles';"
            product_pk = lostQuery(preexisting)
            if not (product_pk):
                insertProduct = "INSERT INTO products(description) VALUES ('Convoy vehicles');"
                inserted = lostQuery(insertProduct)
                product_pk = lostQuery(preexisting)
            preexisting = "SELECT asset_pk from assets where asset_tag='"+vehicle+"';"
            asset_pk = lostQuery(preexisting)
            if not (asset_pk):
                insertAsset = "INSERT INTO assets(product_fk, asset_tag, description, alt_description) VALUES ('"+product_pk+"', '"+vehicle+"', 'A convoy vehicle', 'No further details');"
                inserted = lostQuery(insertAsset)
                asset_pk = lostQuery(preexisting)
            #Insert vehicle/Check return success
            preexisting = "SELECT vehicle_pk from vehicles where asset_fk='"+asset_pk+"';"
            exists = lostQuery(preexisting)
            if not (exists):
                insertNew = "INSERT INTO vehicles(asset_fk) VALUES ('"+asset_pk+"');"
                inserted = lostQuery(insertNew)
                if not (inserted): print("Error, "+vehicle+" not inserted into vehicles")

def facilitiesInsert(lines):
    facilities = [HQ, DC, NC, SPNV, MB005]
    for facility in facilities:
        preexisting = "SELECT facility_pk from facilities where fcode='"+facility+"';"
        facility_pk = lostQuery(preexisting)
        if not (facility_pk)
            insertNew = "INSERT INTO facilities (fcode) VALUES ('"+facility+"');"
            inserted = lostQuery(insertNew)
            if not (inserted): print("Error, "+facility+" not inserted into facilities")

def asset_atInsert(legacy, lines):
    #Find relevant data
    legacy = legacy.split('_')
    fcode = legacy[0]
    preexisting = "SELECT facility_pk from facility where fcode='"+fcode+"';"
    facility_fk = lostQuery(preexisting)
    if not (facility_fk):
        insertNew = "INSERT INTO facilities (fcode) VALUEES ('"+fcode+"');"
        inserted = lostQuery(insertNew)
        facility_fk = lostQuery(preexisting)
    for i in range(len(lines[0])):
        if lines[0][i] == 'asset tag': tag = i
        if lines[0][i] == 'intake date': intake = i
        if lines[0][i] == 'expunged date': expunged = i
    for line in lines(1:):
        preexisting = "SELECT asset_pk from assets where asset_tag='"+line[tag]+"';"
        asset_fk = lostQuery(preexisting)
        if not (asset_fk):
            insertAsset = "INSERT INTO assets(product_fk, asset_tag, description, alt_description) VALUES ('"+product_pk+"', '"+line[tag]+"', 'A convoy vehicle', 'No further details');"
            inserted = lostQuery(insertAsset)
            asset_fk = lostQuery(preexisting)
        preexisting = "SELECT facility_fk from asset_at where asset_fk='"+asset_fk+"';"
        exists = lostQuery(preexisting)
        if not (exists)
            insertNew = "INSERT INTO asset_at(asset_fk, facility_fk, arrive_dt, depart_dt) VALUES ('"+asset_fk+"', '"+facility_fk+"', '"+line[intake]+"', "+line[expunged]+"');"
            inserted = lostQuery(insertNew)
            if not (inserted): print("Error, "+asset_fk+" not inserted into asset_at")

def convoysInsert(lines):
    #Find relevant data
    for i in range(len(lines[0])):
        if lines[0][i] == 'transport request #': request = i
        if lines[0][i] == 'depart time': depart = i
        if lines[0][i] == 'arrive time': arrive = i

    #Check convoy is not already inserted
    preexisting = "SELECT convoy_pk from convoys where request='"+line[request]+"';"
    convoy_pk = lostQuery(preexisting)
    if not (convoy_pk):
        insertNew = "INSERT INTO convoys(request, depart_dt, arrive_dt) VALUES ('"+line[request]+"', '"+line[depart]+"', '"+line[arrive]+"');"
            inserted = lostQuery(insertNew)
            if not (inserted): print("Error, "+line+" not inserted into convoys")

def used_byInsert(lines):
    #Find relevant data
    for i in range(len(lines[0])):
        if lines[0][i] == 'transport request #': request = i
        if lines[0][i] == 'assigned vehicles': vehicles = i
    for line in lines(:1):
        #Check convoy is not already inserted
        for vehicle in line[vehicles]:
            preexisting = "SELECT asset_pk from assets where asset_tag='"+vehicle+"';"
            asset_pk = lostQuery(preexisting)
            preexisting = "SELECT vehicle_pk from vehicles where asset_fk='"+asset_pk+"';"
            vehicle_fk = lostQuery(preexisting)
            preexisting = "SELECT convoy_pk from convoys where request='"+line[request]+"';"
            convoy_fk = lostQuery(preexisting)
            preexisting = "SELECT convoy_fk from used_by where vehicle_fk='"+vehicle_fk+"';"
            exists = lostQuery(preexisting)
            if not (exists)
                insertNew = "INSERT INTO used_by(vehicle_fk, convoy_fk) VALUES ('"+vehicle_fk+"', '"+convoy_fk+"');"
                inserted = lostQuery(insertNew)
                if not (inserted): print("Error, "+vehicle_fk+" not inserted into used_by")

def asset_on(lines):





def updateTables(legacy):
#Tables: 0-products, 1-assets, 2-vehicles, 3-facilities, 4-asset_at, 5-convoys, 6-used_by, 7-asset_on, 8-users, 9-roles, 10-user_is, 11-user_supports, 12-levels, 13-compartments, 14-security_tags
    return {
        'acquisitions': [],
        'convoy':       [False, False, True, False, False, False, True, False, False, False, False, False, False, False, False],
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

def callInsert(tables, legacy, lines):
    if tables[0] == True:
        productsInsert(lines)
    if tables[1] == True:
        assetsInsert(lines)
    if tables[2] == True:
        vehiclesInsert(lines)
    if tables[3] == True:
        facilitiesInsert(lines)
    if tables[4] == True:
        asset_atInsert(legacy, lines)
    if tables[5] == True:
        convoysInsert(lines)
    if tables[6] == True:
        used_byInsert(lines)
    if tables[7] == True:
        asset_onInsert(lines)
    if tables[8] == True:
        usersInsert(lines)
    if tables[9] == True:
        rolesInsert(lines)
    if tables[10] == True:
        user_isInsert(lines)
    if tables[11] == True:
        user_supportsInsert(lines)
    if tables[12] == True:
        levelsInsert(lines)
    if tables[13] == True:
        compartmentsInsert(lines)
    if tables[14] == True:
        security_tagsInsert(lines)
 
# Parse lines
# Grab elements of array line to generate sql statements
# Print SQL statement to insert.sql

#select column_name from information_schema.columns where table_name='assets';
