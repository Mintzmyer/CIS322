#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./preflight.sh <dbname>"
	exit;
fi
# Set up the database tables
psql $1 -f $HOME/CIS322/sql/create_tables.sql
# JUST FOR TESTING remove before submission!!!
#psql $1 -f $HOME/CIS322/sql/testvalues.sql

#Install the wsgi files
cp -R $HOME/CIS322/src/*.py $HOME/wsgi/
cp -R $HOME/CIS322/src/*.html $HOME/wsgi/templates/

# Modify app.py to specified DB name
match='currentDB='
insert="currentDB='"$1"' #"
file='app.py'

sed -i "s/$match/$insert/" $HOME/wsgi/$file

# JUST FOR TESTING remove before submission!!!
#apachectl restart
