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

# Import transfers.csv file and split data into increments
def parseFile(csvFile):
    with open(csvFile) as table:
        lines = table.readlines()
    for i, line in enumerate(lines):
        lines[i]=line.split(',')
    uploadTransfers(lines)

    table.close()

# Accepts parsed data and traverses it into sql insert statement
def uploadTransfers(arrayData):
    #Verify data location in header
    for i in range(len(arrayData[0])):
        if ('asset_tag' in arrayData[0][i]): atag=i
        if ('request_by' in arrayData[0][i]): reqby=i
        if ('request_dt' in arrayData[0][i]): reqdt=i
        if ('approve_by' in arrayData[0][i]): appby=i
        if ('approve_dt' in arrayData[0][i]): appdt=i
        if ('source' in arrayData[0][i]): source=i
        if ('destination' in arrayData[0][i]): dest=i
        if ('load_dt' in arrayData[0][i]): load=i
        if ('unload_dt' in arrayData[0][i]): unload=i
        print(arrayData[0][i])

    for line in arrayData[1:]:
        print(line)
        sqlTransfer="INSERT INTO transfer_request (date_requested, date_approved, requester_fk, approver_fk) SELECT %s, %s, u.user_pk, v.user_pk FROM (SELECT user_pk from users WHERE username=%s) as u cross join (SELECT user_pk FROM users WHERE username=%s) as v;"
        lostQuery(sqlTransfer, (line[reqdt], line[appdt], line[reqby], line[appby]))
        sqlRequestFk="SELECT max(request_pk) from transfer_request where (date_requested=%s AND date_approved=%s);"
        requestPk=lostQuery(sqlRequestFk, (line[reqdt], line[appdt]))[0][0]
        if ('None' in line[load]): load_dt=None
        else: load_dt=line[load]
        if ('None' in line[unload]): unload_dt=None
        else: unload_dt=line[unload]
        sqlATransfers="INSERT INTO asset_transfers (request_fk, load, unload, asset_fk, source_fk, destination_fk) SELECT %s, %s, %s, a.asset_pk, f.facility_pk, g.facility_pk FROM (SELECT asset_pk from assets where tag=%s) as a CROSS JOIN (SELECT facility_pk from facilities where code=%s) as f CROSS JOIN (SELECT facility_pk from facilities where code=%s) as g;"
        lostQuery(sqlATransfers, (requestPk, load_dt, unload_dt, line[atag], line[source], line[dest]))

if not (len(sys.argv)==3):
    print("usage: transfersUp.py <db name> <input dir>")
    quit()

path=sys.argv[2]
if not (path[-1]=='/'):
    path=path+'/'
csvTransfers=path+'transfers.csv'
parseFile(csvTransfers)
