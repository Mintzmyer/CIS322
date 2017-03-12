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

f = open('assets.csv', 'w')

# Write header for file
header = "asset_tag, description, facility, acquired, disposed\n"
f.write(header) #Convert to string?

# Collect users data in mass array dump
#sqlAssetDump="SELECT a.tag, a.description, f.name, min(al.arrival), CASE WHEN al.facility_fk='1' THEN al.arrival END AS disposed FROM assets as a inner join asset_location as al on a.asset_pk=al.asset_fk inner join facilities as f on al.facility_fk=f.facility_pk GROUP BY a.tag, a.description, f.name, al.facility_fk, al.arrival;"
sqlAssetDump="SELECT a.tag, a.description, f.name, t.arrival, CASE WHEN al.facility_fk='1' THEN al.arrival END AS disposed FROM (SELECT a.tag, min(al.arrival) as arrival FROM assets as a inner join asset_location as al on a.asset_pk=al.asset_fk GROUP BY a.tag) AS t INNER JOIN assets AS a on a.tag=t.tag INNER JOIN asset_location as al on a.asset_pk=al.asset_fk INNER JOIN facilities as f on al.facility_fk=f.facility_pk;"
assets=lostQuery(sqlAssetDump, (None,))

# Loop through array, writing each line to .csv file
assetline="%s, %s, %s, %s, %s\n"
for asset in assets:
    # Skip entry if it only communicates disposal
    if (asset[4]):
        continue
    #If entry has no disposal date, check if a disposal entry exists
    if not (asset[4]):
        found=False
        for line in assets:
            if ((asset[0]==line[0]) and (line[4])):
                f.write(assetline % (asset[0], asset[1], asset[2], asset[3], line[4]))
                found=True
        if not found:
            f.write(assetline % (asset[0], asset[1], asset[2], asset[3], asset[4]))

# Close file
f.close()
