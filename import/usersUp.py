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

# Import users.csv file and split data into increments
def parseFile(csvFile):
    with open(csvFile) as table:
        lines = table.readlines()
    for i, line in enumerate(lines):
        lines[i]=line.split(',')
    uploadUsers(lines)

    table.close()

# Accepts parsed data and traverses it into sql insert statement
def uploadUsers(arrayData):
    #Verify data location in header
    for i in range(len(arrayData[0])):
        if ('username' in arrayData[0][i]): uname=i
        if ('password' in arrayData[0][i]): upass=i
        if ('role' in arrayData[0][i]): urole=i
        if ('active' in arrayData[0][i]): uactive=i
        print(arrayData[0][i])

    for line in arrayData[1:]:
        print(line)
        sqlUser="INSERT INTO users (username, password, active, role_fk) SELECT %s, %s, %s, role_pk from roles where title=%s;"
            #sqlAssetLoc="INSERT INTO asset_location(asset_fk, arrival, departure, facility_fk) SELECT %s, %s, %s, facility_pk from facilities where facilities.code=%s;"
        lostQuery(sqlUser, (line[uname], line[upass], line[uactive].strip(), line[urole]))

if not (len(sys.argv)==3):
    print("usage: usersUp.py <db name> <input dir>")
    quit()

path=sys.argv[2]
if not (path[-1]=='/'):
    path=path+'/'
csvUsers=path+'users.csv'
parseFile(csvUsers)
