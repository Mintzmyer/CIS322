import psycopg2
import sys

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

# Get arguments for file name to write to
if not (len(sys.argv)==3):
    print("usage: facilitiesDump.py <db name> <output dir>")
    quit()
path=sys.argv[2]
if not (path[-1]=='/'):
    path=path+'/'
path=path+'facilities.csv'

f = open(path, 'w')

# Write header for file
header = "fcode,common_name\n"
f.write(header) #Convert to string?

# Collect facilities data in mass array dump
sqlFacilityDump="SELECT code, name FROM facilities;"
facilities=lostQuery(sqlFacilityDump, (None,))

# Loop through array, writing each line to .csv file
facilityline="%s,%s\n"
for facility in facilities:
    f.write(facilityline % (facility[0], facility[1]))

# Close file
f.close()
