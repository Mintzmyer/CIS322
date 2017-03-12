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

f = open('transfers.csv', 'w')

# Write header for file
header = "asset_tag, request_by, request_dt, approve_by, approve_dt, source, destination, load_dt, unload_dt\n"
f.write(header)

# Collect transfer data in mass array dump
sqlTransferDump="SELECT a.tag, tr.requester_fk, tr.date_requested, tr.approver_fk, tr.date_approved, at.source_fk, at.destination_fk, at.load, at.unload FROM assets as a inner join asset_transfers as at on a.asset_pk=at.asset_fk inner join transfer_request as tr on at.request_fk=tr.request_pk;"
transfers=lostQuery(sqlTransferDump, (None,))

# Loop through array, writing each line to .csv file
transferline="%s, %s, %s, %s, %s, %s, %s, %s, %s\n"
for transfer in transfers:
    f.write(transferline % (transfer[0], transfer[1], transfer[2], transfer[3], transfer[4], transfer[5], transfer[6], transfer[7], transfer[8]))

# Close file
f.close()
