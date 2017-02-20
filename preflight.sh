#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: ./preflight.sh <dbname>"
	exit;
fi

# Set up the database tables
cd sql
psql $1 -f create_tables.sql
cd ..

#Install the wsgi files
cp -R src/*.py $HOME/wsgi/
cp -R src/*.html $HOME/wsgi/templates/

apachectl restart

