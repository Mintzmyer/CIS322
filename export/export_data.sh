#!/usr/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: ./export_data.sh <dbname> <output dir>"
	exit;
fi

# <dbname> Running on localhost 127.0.0.1 at port 5432
# <output dir> Path where data files should be read from. If DNE, create dir. If Exists, rm content

# users.csv - a csv file containing user information
# facilities.csv - a csv file containing LOST facility information
# assets.csv - a csv file containing LOST assets
# transfers.csv - a csv file containing transfer information


# Set up the database tables
cd sql
psql $1 -f create_tables.sql
# JUST FOR TESTING remove before submission!!!
#psql $1 -f testvalues.sql
cd ..

#Install the wsgi files
cp -R src/*.py $HOME/wsgi/
cp -R src/*.html $HOME/wsgi/templates/

# JUST FOR TESTING remove before submission!!!
#apachectl restart
