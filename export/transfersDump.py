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
    print("usage: transfersDump.py <db name> <output dir>")
    quit()
path=sys.argv[2]
if not (path[-1]=='/'):
    path=path+'/'
path=path+'transfers.csv'

f = open(path, 'w')

# Write header for file
header = "asset_tag,request_by,request_dt,approve_by,approve_dt,source,destination,load_dt,unload_dt\n"
f.write(header)

# Collect transfer data in mass array dump
sqlTransferDump="SELECT a.tag, u.username, tr.date_requested, v.username, tr.date_approved, f.code, g.code, at.load, at.unload FROM assets as a inner join asset_transfers as at on a.asset_pk=at.asset_fk inner join transfer_request as tr on at.request_fk=tr.request_pk inner join users as u on tr.requester_fk=u.user_pk inner join users as v on tr.approver_fk=v.user_pk inner join facilities as f on at.source_fk=f.facility_pk inner join facilities as g on at.source_fk=g.facility_pk;"
transfers=lostQuery(sqlTransferDump, (None,))

# Loop through array, writing each line to .csv file
transferline="%s,%s,%s,%s,%s,%s,%s,%s,%s\n"
for transfer in transfers:
    f.write(transferline % (transfer[0], transfer[1], transfer[2], transfer[3], transfer[4], transfer[5], transfer[6], transfer[7], transfer[8]))

# Close file
f.close()
