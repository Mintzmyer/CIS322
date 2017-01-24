#! /usr/bin/bash

cp $HOME/CIS322/src/*.html $HOME/wsgi/templates/
cp $HOME/CIS322/app.py $HOME/wsgi/

apachectl restart
