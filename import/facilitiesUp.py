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

# Import facilities.csv file and split data into increments
def parseFile(csvFile):
    with open(csvFile) as table:
        lines = table.readlines()
    for i, line in enumerate(lines):
        lines[i]=line.split(',')
    uploadFacilities(lines)

    table.close()

# Accepts parsed data and traverses it into sql insert statement
def uploadFacilities(arrayData):
    #Verify data location in header
    for i in range(len(arrayData[0])):
        if ('fcode' in arrayData[0][i]): fcode=i
        if ('common_name' in arrayData[0][i]): fname=i
        print(arrayData[0][i])

    for line in arrayData[1:]:
        print(line)
        sqlFacility="INSERT INTO facilities (code, name) VALUES (%s, %s);"
        lostQuery(sqlFacility, (line[fcode], line[fname].strip()))

# Check argument length, pass .csv file to parser
if not (len(sys.argv)==3):
    print("usage: facilitiesUp.py <db name> <input dir>")
    quit()
csvFacilities=sys.argv[2]
parseFile(csvFacilities)
