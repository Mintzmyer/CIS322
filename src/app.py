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
                #sqlRole="SELECT role from users where user_pk='"%s"';"
                #session['role']=lostQuery(sqlRole,(userPk))

        return redirect(url_for('dashboard'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method=='GET':
        sqlRoles="SELECT role_pk, title from roles;"
        roles_list=lostQuery(sqlRoles)
        return render_template('create_user.html', roles_list=roles_list)
    
    if request.method=='POST' and 'username' and 'password' in request.form:
        username=request.form.get('username')
        password=request.form.get('password')
        role=request.form.get('role')

        #Check DB for existing user
        sqlUser="SELECT user_pk from users where username='"+username+"';"
        userPk=lostQuery(sqlUser)
        
        #If user does not exist, insert submitted data into users table
        if not (userPk):
            sqlNewUser="INSERT INTO users(username, password, role_fk) VALUES ('"+username+"', '"+password+"', '"+role+"');"
            lostQuery(sqlNewUser)    
            sqlUser="SELECT user_pk from users where username='"+username+"';"
            userPk=str(lostQuery(sqlUser)[0][0])
            #Query new submission for session username
            sqlUsername="SELECT username from users where user_Pk='"+userPk+"';"
            session['user']=str(lostQuery(sqlUsername)[0][0])
            #session['role']=role
        
        #If user already exists, report that.
        else:
            session['user']="already registered."

        #Redirect to dashboard where the username is proudly displayed
        return redirect(url_for('dashboard'))

@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    sqlFacilities=("SELECT name, code FROM facilities")
    if request.method=='GET':
        msg="Ready to add a facility"
        facilities_list=lostQuery(sqlFacilities)
        return render_template('add_facility.html', facilities_list=facilities_list, add_message=msg)

    if request.method=='POST':
        fname=request.form.get('fname')
        fcode=request.form.get('fcode')
        sqlFName="SELECT facility_pk FROM facilities where name='"+fname+"';"
        nameTaken=lostQuery(sqlFName)
        if not (nameTaken):
            sqlFCode="SELECT facility_pk FROM facilities where code='"+fcode+"';"
            codeTaken=lostQuery(sqlFCode)
            if not (codeTaken):
                sqlNewf="INSERT INTO facilities(name, code) VALUES ('"+fname+"', '"+fcode+"');"
                lostQuery(sqlNewf)
                msg="Facility successfuly added"
            else:
                msg="A facility already has that code"
        else:
            msg="A facility already has that name"
        facilities_list=lostQuery(sqlFacilities)
        return render_template('add_facility.html', facilities_list=facilities_list, add_message=msg)

@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    sqlFacilities=("SELECT facility_pk, name FROM facilities")
    sqlAssets=("SELECT a.tag, a.description, f.name from assets as a inner join asset_location as ao on a.asset_pk=ao.asset_fk inner join facilities as f on ao.facility_fk=f.facility_pk")
    facilities_list=lostQuery(sqlFacilities)
    
    if request.method=='GET':
        msg="Ready to add an asset"
        assets_list=lostQuery(sqlAssets)
        return render_template('add_asset.html', assets_list=assets_list, facilities_list=facilities_list)

    if request.method=='POST':
        atag=request.form.get('atag')
        adescription=request.form.get('adesc')
        arrival=request.form.get('arrival')
        facility=request.form.get('facilities')
        sqlAtag="SELECT asset_pk FROM assets where tag='"+atag+"';"
        tagTaken=lostQuery(sqlAtag)
        if not (tagTaken):
            sqlNewa="INSERT INTO assets(tag, description) VALUES ('"+atag+"', '"+adescription+"');"
            lostQuery(sqlNewa)
            sqlApk="SELECT asset_pk from assets where tag='"+atag+"';"
            asset_pk=lostQuery(sqlApk)
            sqlNewLocation="INSERT INTO asset_location(asset_fk, facility_fk, arrival) VALUES ('"+str(asset_pk[0][0])+"', '"+str(facility)+"', '"+str(arrival)+"');"
            lostQuery(sqlNewLocation)
            msg="Asset successfully added"
        else:
            msg="A asset already has that tag"
        assets_list=lostQuery(sqlAssets)
        return render_template('add_asset.html', assets_list=assets_list, facilities_list=facilities_list)

@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    sqlRole="SELECT r.title from roles as r inner join users as u on u.role_fk=r.role_pk where u.name='%s';"
    role=lostQuery(sqlRole,(session[user]))
    if not (role="Logistics Officer"):
        msg="required to have the role of Logistics Officer to dispose of assets"
        return render_template('dashboard.html', usermsg=msg)
    if request.method=='GET':
        msg="User cleared to register dispose assets"
        return render_template('dispose_asset.html', dispose_msg=msg)
    if request.method=='POST':
        atag=request.form.get('atag')
        sqlExist="SELECT asset_pk from assets where tag='%s';"
        assetPk=lostQuery(sqlExist, (atag))
        if not (location):
            msg="There is no asset that matches that tag"
        else:
            sqlTrash="SELECT al.arrival from asset_location as al inner join facility as f on f.facility_pk=ao.facility_fk where al.asset_fk='%s' and f.code='Trash';"
            #sqlLocate="SELECT f.code from facility as f inner join asset_location as ao on f.facility_pk=ao.facility_fk where ao.asset_fk='%s' and f.code='Trash';"
            disposed=lostQuery(sqlTrash, (assetPk))
            if (disposed):
                msg="That asset has already been disposed of"
            else: 
                now = CurrentDate()
                sqlDispose="INSERT INTO asset_location(asset_fk, facility_fk, arrival) select %s, facility_pk from facilities where facilities.code='Trash', %s;"
                lostQuery(sqlDispose, (assetPk, now))
                msg="Asset listed as disposed"
        return render_template('dispose_asset.html', dispose_msg=msg)



@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', usermsg=session['user'])

@app.route('/logout')
def logout():
    return redirect(url_for('login'))
