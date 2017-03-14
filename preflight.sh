#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./preflight.sh <dbname>"
	exit;
fi
# Set up the database tables
cd sql
psql $1 -f create_tables.sql
# JUST FOR TESTING remove before submission!!!
#psql $1 -f testvalues.sql
cd ..

#Install the wsgi files
cp -R src/*.py $HOME/wsgi/
cp -R src/*.html $HOME/wsgi/templates/

# Modify app.py to specified DB name
match='currentDB='
insert="currentDB='"$1"' #"
file='app.py'

sed -i "s/$match/$insert/" $HOME/wsgi/$file

# JUST FOR TESTING remove before submission!!!
#apachectl restart
