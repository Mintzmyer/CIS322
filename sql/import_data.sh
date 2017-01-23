#! /usr/bin/bash

mkdir $HOME/LegacyTar
cd $HOME/LegacyTar

curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > osnap_legacy.tar.gz
cd $HOME
tar xvf LegacyTar/osnap_legacy.tar.gz

rm -r LegacyTar

psql postgres -f $HOME/CIS322/sql/create_tables.sql 
