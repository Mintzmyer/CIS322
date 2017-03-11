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

f = open('users.csv', 'w')

# Write header for file
header = "username, password, role, active\n"
f.write(header) #Convert to string?

# Collect users data in mass array dump
sqlUserDump="SELECT username, password, role_fk, active FROM users;"
users=lostQuery(sqlUserDump, (None,))

# Loop through array, 

