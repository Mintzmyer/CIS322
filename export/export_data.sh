#!/usr/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./export_data.sh <dbname> <output dir>"
	exit;
fi

# <dbname> Running on localhost 127.0.0.1 at port 5432
# <output dir> Path where data files should be read from. If DNE, create dir. If Exists, rm content



# users.csv - a csv file containing user information
python usersDump.py
# facilities.csv - a csv file containing LOST facility information
python facilitiesDump.py
# assets.csv - a csv file containing LOST assets
python assetsDump.py
# transfers.csv - a csv file containing transfer information
python transfersDump.py
