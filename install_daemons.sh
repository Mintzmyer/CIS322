#! /usr/bin/bash

mkdir $HOME/installed

github clone https://github.com/postgres/postgres.git
cd $HOME/postgres
$HOME/postgres/configure --prefix=$HOME/installed
make
make install

curl http://download.nextag.com/apache//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25.tar.bz2

cd $HOME/httpd-2.4.25.tar.bz2
$HOME/httpd-2.4.25/configure --prefix=$HOME/installed
make
make install

cd $HOME
rm -rf $HOME/postgres
rm -rf $HOME/httpd-2.4.25
rm -rf $HOME/httpd-2.4.25.tar.bz2




