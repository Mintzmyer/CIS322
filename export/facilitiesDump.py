import psycopg2
from sys import argv


def lostQuery(sqlQuery, params):
    conn = psycopg2.connect("dbname='lost' user='osnapdev' host='127.0.0.1'")
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

f = open('facilities.csv', 'w')

# Write header for file
header = "fcode, common_name\n"
f.write(header) #Convert to string?

# Collect facilities data in mass array dump
sqlFacilityDump="SELECT code, name FROM facilities;"
facilities=lostQuery(sqlFacilityDump, (None,))

# Loop through array, writing each line to .csv file
facilityline="%s, %s\n"
for facility in facilities:
    f.write(facilityline % (facility[0], facility[1]))

# Close file
f.close()
