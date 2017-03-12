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

# Get arguments for file name to write to
if not (len(sys.argv)==3):
    print("usage: usersDump.py <db name> <output dir>")
    quit()
path=sys.argv[2]
if not (path[-1]=='/'):
    path=path+'/'
path=path+'users.csv'

f = open(path, 'w')

# Write header for file
header = "username,password,role,active\n"
f.write(header) #Convert to string?

# Collect users data in mass array dump
sqlUserDump="SELECT username, password, r.title, active FROM users inner join roles as r on users.role_fk=r.role_pk;"
users=lostQuery(sqlUserDump, (None,))

# Loop through array, writing each line to .csv file
userline="%s,%s,%s,%s\n"
for user in users:
    f.write(userline % (user[0], user[1], user[2], user[3]))

# Close file
f.close()


