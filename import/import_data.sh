#!/usr/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: bash import_data.sh <dbname> <input dir>"
	exit;
fi

# <dbname> DB to import data into. Run on localhost 127.0.0.1 port 5432
# <input dir> Path to dir where data files should be read from

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
