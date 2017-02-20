from flask import Flask, render_template, request, redirect, url_for, session
from picklesession import PickleSessionInterface
import psycopg2
import os
import json
import datetime


global SECRET_KEY

SECRET_KEY = 'a0z987asdf'

app = Flask(__name__)
app.secret_key = SECRET_KEY


path='/dev/shm/lost_sessions'
if not os.path.exists(path):
    os.mkdir(path)
    os.chmod(path, int('700',8))
app.session_interface=PickleSessionInterface(path)

def lostQuery(sqlQuery):
    conn = psycopg2.connect("dbname='lost' user='osnapdev' host='127.0.0.1'")
    #print("conn:"+str(conn))
    cur = conn.cursor()
    #print("cur:"+str(cur))
    print(sqlQuery)
    cur.execute(sqlQuery)
    try:
        result = cur.fetchall()
    except psycopg2.ProgrammingError:
        result = ''
    print("Result:"+str(result))
    conn.commit()
    cur.close()
    conn.close()
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    
    if request.method=='POST' and 'username' and 'password' in request.form:
        username=request.form.get('username')
        password=request.form.get('password')

        #Check login credentials
        sqlUser="SELECT user_pk from users where username='"+username+"';"
        userPk=lostQuery(sqlUser)

        #If username doesn't exist, report that
        if not (userPk):
            session['user']="not registered"

        #If username exists, check password
        else:
            sqlPassword="SELECT user_pk from users where username='"+username+"' and password='"+password+"';"
            login=lostQuery(sqlPassword)
            
            #If login fails, report wrong password. Otherwise, report username
            if not (login):
                session['user']="associated with a different password"
            else:
                session['user']=username

        return redirect(url_for('dashboard'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method=='GET':
        return render_template('create_user.html')
    
    if request.method=='POST' and 'username' and 'password' in request.form:
        username=request.form.get('username')
        password=request.form.get('password')

        #Check DB for existing user
        sqlUser="SELECT user_pk from users where username='"+username+"';"
        userPk=lostQuery(sqlUser)
        
        #If user does not exist, insert submitted data into users table
        if not (userPk):
            sqlNewUser="INSERT INTO users(username, password) VALUES ('"+username+"', '"+password+"');"
            lostQuery(sqlNewUser)    
            sqlUser="SELECT user_pk from users where username='"+username+"';"
            userPk=str(lostQuery(sqlUser)[0][0])
            #Query new submission for session username
            sqlUsername="SELECT username from users where user_Pk='"+userPk+"';"
            session['user']=str(lostQuery(sqlUsername)[0][0])
        
        #If user already exists, report that.
        else:
            session['user']="already registered."

        #Redirect to dashboard where the username is proudly displayed
        return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', username=session['user'])

@app.route('/logout')
def logout():
    return redirect(url_for('login'))
