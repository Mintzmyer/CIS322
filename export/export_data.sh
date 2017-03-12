#!/usr/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./export_data.sh <dbname> <output dir>"
	exit;
fi

# <dbname> Running on localhost 127.0.0.1 at port 5432
# <output dir> Path where data files should be read from. If DNE, create dir. If Exists, rm content



# users.csv - a csv file containing user information
[ -f $2/users.csv ] && rm $2/users.csv
python usersDump.py $1 $2

# facilities.csv - a csv file containing LOST facility information
[ -f $2/facilities.csv ] && rm $2/facilities.csv
python facilitiesDump.py $1 $2

# assets.csv - a csv file containing LOST assets
[ -f $2/assets.csv ] && rm $2/assets.csv
python assetsDump.py $1 $2

# transfers.csv - a csv file containing transfer information
[ -f $2/transfers.csv ] && rm $2/transfers.csv
python transfersDump.py $1 $2
