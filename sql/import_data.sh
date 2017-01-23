#! /usr/bin/bash

mkdir $HOME/LegacyTar
cd $HOME/LegacyTar

curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > osnap_legacy.tar.gz
cd $HOME
tar xvf LegacyTar/osnap_legacy.tar.gz

rm -r LegacyTar

initdb d
pg_ctl -D d -l logfile start

psql postgres -f $HOME/CIS322/sql/create_tables.sql 

python3 $HOME/CIS322/sql/gen_insert.py

