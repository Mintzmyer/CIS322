import psycopg2
import sys
#from sys import argv


def lostQuery(sqlQuery, params):
    conn = psycopg2.connect("dbname='"+sys.argv[1]+"' user='osnapdev' host='127.0.0.1'")
    cur = conn.cursor()
    if not (params):
        cur.execute(sqlQuery)
    else:
        cur.execute(sqlQuery, params)
    try:
        result = cur.fetchall()
    except psycopg2.ProgrammingError:
        result = ''
    conn.commit()
    cur.close()
    conn.close()
    return result

# Import assets.csv file and split data into increments
def parseFile(csvFile):
    with open(csvFile) as table:
        lines = table.readlines()
    for i, line in enumerate(lines):
        lines[i]=line.split(',')
    uploadAssets(lines)

    table.close()

# Accepts parsed data and traverses it into sql insert statement
def uploadAssets(arrayData):
    #Verify data location in header
    for i in range(len(arrayData[0])):
        if ('asset_tag' in arrayData[0][i]): atag=i
        if ('description' in arrayData[0][i]): adesc=i
        if ('facility' in arrayData[0][i]): afacility=i
        if ('acquired' in arrayData[0][i]): acquired=i
        if ('disposed' in arrayData[0][i]): disposed=i
        print(arrayData[0][i])

    for line in arrayData[1:]:
        print(line)
        sqlAsset="INSERT INTO assets (tag, description) VALUES (%s, %s);"
        lostQuery(sqlAsset, (line[atag], line[adesc]))
        sqlApk="SELECT asset_pk from assets where tag=%s;"
        asset_pk=lostQuery(sqlApk, (line[atag],))
        # If asset is disposed, add departure date and enter it into 'Disposed' location
        if not (line[disposed]=='None\n'):
            sqlAssetLoc="INSERT INTO asset_location(asset_fk, arrival, departure, facility_fk) SELECT %s, %s, %s, facility_pk from facilities where facilities.code=%s;"
            lostQuery(sqlAssetLoc, (str(asset_pk[0][0]), line[acquired], line[disposed], line[afacility]))
            sqlDispose="INSERT INTO asset_location(asset_fk, arrival, facility_fk) select %s, %s, facility_pk from facilities where facilities.code='Trash';"
            lostQuery(sqlDispose, (str(asset_pk[0][0]), line[disposed]))
        else:
            sqlAssetLoc="INSERT INTO asset_location(asset_fk, arrival, facility_fk) SELECT %s, %s, facility_pk from facilities where facilities.code=%s;"
            lostQuery(sqlAssetLoc, (str(asset_pk[0][0]), line[acquired], line[afacility]))

if not (len(sys.argv)==3):
    print("usage: assetsUp.py <db name> <input dir>")
    quit()
csvAssets=sys.argv[2]
parseFile(csvAssets)
