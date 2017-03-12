#!/usr/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./import_data.sh <dbname> <output dir>"
	exit;
fi

# <dbname> Running on localhost 127.0.0.1 at port 5432
# <output dir> Path where data files should be read from. If DNE, shoot it'll probably crash.



# users.csv - a csv file containing user information
python usersUp.py $1 $2

# facilities.csv - a csv file containing LOST facility information
python facilitiesUp.py $1 $2

# assets.csv - a csv file containing LOST assets
python assetsUp.py $1 $2

# transfers.csv - a csv file containing transfer information
python transfersUp.py $1 $2
