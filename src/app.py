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

def lostQuery(sqlQuery, params):
    conn = psycopg2.connect("dbname='lost' user='osnapdev' host='127.0.0.1'")
    #print("conn:"+str(conn))
    cur = conn.cursor()
    #print("cur:"+str(cur))
    #print(sqlQuery)
    if not (params):
        cur.execute(sqlQuery)
    else:
        cur.execute(sqlQuery, params)
    try:
        result = cur.fetchall()
    except psycopg2.ProgrammingError:
        result = ''
    #print("Result:"+str(result))
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
        session['msg']="Please enter your username and password"
        return render_template('login.html', login_msg=session['msg'])
    
    if request.method=='POST' and 'username' and 'password' in request.form:
        username=request.form.get('username')
        password=request.form.get('password')

        #Check login credentials
        sqlUser="SELECT user_pk from users where username=%s;"
        userPk=lostQuery(sqlUser, (username,))

        #If username doesn't exist, report that
        if not (userPk):
            session['msg']="Username is not registered"
            return render_template('login.html', login_msg=session['msg'])

        #If username exists, check password
        else:
            sqlPassword="SELECT user_pk from users where username=%s and password=%s;"
            login=lostQuery(sqlPassword, (username, password))
            
            #If login fails, report wrong password. Otherwise, report username
            if not (login):
                session['msg']="Username associated with a different password"
                return render_template('login.html', login_msg=session['msg'])
            else:
                session['user']=username
                #sqlRole="SELECT role from users where user_pk='"%s"';"
                #session['role']=lostQuery(sqlRole,(userPk))

        return redirect(url_for('dashboard'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    sqlRoles="SELECT role_pk, title from roles;"
    roles_list=lostQuery(sqlRoles, None)
    if request.method=='GET':
        session['msg']="Please create your username and password:"
        return render_template('create_user.html', roles_list=roles_list, create_msg=session['msg'])
    
    if request.method=='POST' and 'username' and 'password' in request.form:
        username=request.form.get('username')
        password=request.form.get('password')
        role=request.form.get('role')

        #Check DB for existing user
        sqlUser="SELECT user_pk from users where username=%s;"
        userPk=lostQuery(sqlUser, (username,))
        
        #If user does not exist, insert submitted data into users table
        if not (userPk):
            sqlNewUser="INSERT INTO users(username, password, role_fk) VALUES (%s, %s, %s);"
            lostQuery(sqlNewUser, (username, password, role))    
            sqlUser="SELECT user_pk from users where username=%s;"
            userPk=str(lostQuery(sqlUser, (username,))[0][0])
            #Query new submission for session username
            sqlUsername="SELECT username from users where user_Pk=%s;"
            session['user']=str(lostQuery(sqlUsername, (userPk,))[0][0])
            #session['role']=role
        
        #If user already exists, report that.
        else:
            session['msg']="Username already registered."
            return render_template('create_user.html', roles_list=roles_list, create_msg=session['msg'])

        #Redirect to dashboard where the username is proudly displayed
        return redirect(url_for('dashboard'))

@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
    sqlFacilities=("SELECT name, code FROM facilities")
    if request.method=='GET':
        session['msg']="Ready to add a facility"
        facilities_list=lostQuery(sqlFacilities, None)
        return render_template('add_facility.html', facilities_list=facilities_list, add_message=session['msg'])

    if request.method=='POST':
        fname=request.form.get('fname')
        fcode=request.form.get('fcode')
        sqlFName="SELECT facility_pk FROM facilities where name=%s;"
        nameTaken=lostQuery(sqlFName, (fname,))
        if not (nameTaken):
            sqlFCode="SELECT facility_pk FROM facilities where code=%s;"
            codeTaken=lostQuery(sqlFCode, (fcode,))
            if not (codeTaken):
                sqlNewf="INSERT INTO facilities(name, code) VALUES (%s, %s);"
                lostQuery(sqlNewf, (fname, fcode))
                session['msg']="Facility successfuly added"
            else:
                session['msg']="A facility already has that code"
        else:
            session['msg']="A facility already has that name"
        facilities_list=lostQuery(sqlFacilities, None)
        return render_template('add_facility.html', facilities_list=facilities_list, add_message=session['msg'])

@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    sqlFacilities=("SELECT facility_pk, name FROM facilities")
    sqlAssets=("SELECT a.tag, a.description, f.name from assets as a inner join asset_location as ao on a.asset_pk=ao.asset_fk inner join facilities as f on ao.facility_fk=f.facility_pk")
    facilities_list=lostQuery(sqlFacilities, None)
    
    if request.method=='GET':
        session['msg']="Ready to add an asset"
        assets_list=lostQuery(sqlAssets, None)
        return render_template('add_asset.html', add_message=session['msg'], assets_list=assets_list, facilities_list=facilities_list)

    if request.method=='POST':
        atag=request.form.get('atag')
        adescription=request.form.get('adesc')
        arrival=request.form.get('arrival')
        facility=request.form.get('facilities')
        sqlAtag="SELECT asset_pk FROM assets where tag=%s;"
        tagTaken=lostQuery(sqlAtag, (atag,))
        if not (tagTaken):
            sqlNewa="INSERT INTO assets(tag, description) VALUES (%s, %s);"
            lostQuery(sqlNewa, (atag, adescription))
            sqlApk="SELECT asset_pk from assets where tag=%s;"
            asset_pk=lostQuery(sqlApk, (atag,))
            sqlNewLocation="INSERT INTO asset_location(asset_fk, facility_fk, arrival) VALUES (%s, %s, %s);"
            lostQuery(sqlNewLocation, (str(asset_pk[0][0]), str(facility), str(arrival)))
            session['msg']="Asset successfully added"
        else:
            session['msg']="A asset already has that tag"
        assets_list=lostQuery(sqlAssets, None)
        return render_template('add_asset.html', add_message=session['msg'], assets_list=assets_list, facilities_list=facilities_list)

@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
    sqlRole="SELECT r.title from roles as r inner join users as u on u.role_fk=r.role_pk where u.username=%s;"
    role=lostQuery(sqlRole,(session['user'],))
    if not (role):
        session['msg']="required to dispose of assets"
        return redirect(url_for('dashboard'))
    if not (role[0][0]=="Logistics Officer"):
        session['msg']="required to have the role of Logistics Officer to dispose of assets"
        return redirect(url_for('dashboard'))
    if request.method=='GET':
        session['msg']="User cleared to register dispose assets"
        return render_template('dispose_asset.html', dispose_msg=session['msg'])

    if request.method=='POST':
        atag=request.form.get('atag')
        dday=request.form.get('disposedday')
        sqlExist="SELECT asset_pk from assets where tag=%s;"
        assetPk=lostQuery(sqlExist, (atag,))
        if not (assetPk):
            session['msg']="There is no asset that matches that tag"
        else:
            sqlTrash="SELECT al.arrival from asset_location as al inner join facilities as f on f.facility_pk=al.facility_fk where al.asset_fk=%s and f.code='Trash';"
            #sqlLocate="SELECT f.code from facility as f inner join asset_location as ao on f.facility_pk=ao.facility_fk where ao.asset_fk='%s' and f.code='Trash';"
            disposed=lostQuery(sqlTrash, (assetPk[0][0],))
            if (disposed):
                session['msg']="That asset has already been disposed of"
            else:
                sqlDeparture="UPDATE asset_location set departure=%s where departure is NULL and asset_fk=%s"
                lostQuery(sqlDeparture, (dday, assetPk[0][0]))
                sqlDispose="INSERT INTO asset_location(asset_fk, arrival, facility_fk) select %s, %s, facility_pk from facilities where facilities.code='Trash';"
                lostQuery(sqlDispose, (assetPk[0][0], dday))
                session['msg']="Asset successfully listed as disposed"
        return render_template('dispose_asset.html', dispose_msg=session['msg'])

@app.route('/asset_report', methods=['GET', 'POST'])
def asset_report():
    sqlFacilities=("SELECT facility_pk, name FROM facilities")
    facilities_list=lostQuery(sqlFacilities, None)
    if request.method=='GET':
        session['msg']="You may specify which day and any (or all) facility:"
        blank=iter([])
        return render_template('asset_report.html', report_msg=session['msg'], facilities_list=facilities_list, report_list=blank)
    if request.method=='POST':
        facility=request.form.get('facility')
        day=request.form.get('reportday')
        if (facility=='0'):
            sqlReport="SELECT a.tag, a.description, f.name, al.arrival, al.departure from assets as a inner join asset_location as al on a.asset_pk=al.asset_fk inner join facilities as f on al.facility_fk=f.facility_pk where al.arrival<=%s and (al.departure>=%s or al.departure is NULL);"
            report_list=lostQuery(sqlReport, (day, day))
        else:
            sqlReport="SELECT a.tag, a.description, f.name, al.arrival, al.departure from assets as a inner join asset_location as al on a.asset_pk=al.asset_fk inner join facilities as f on al.facility_fk=f.facility_pk where facility_pk=%s and al.arrival<=%s and (al.departure>=%s or al.departure is NULL)"
            report_list=lostQuery(sqlReport, (facility, day, day))
        session['msg']="Report generated:"
        return render_template('asset_report.html', report_msg=session['msg'], facilities_list=facilities_list, report_list=report_list)

@app.route('/transfer_req', methods=['GET', 'POST'])
def transfer_req():
    # Check user is a logistics officer
    sqlRole="SELECT r.title from roles as r inner join users as u on u.role_fk=r.role_pk where u.username=%s;"
    role=lostQuery(sqlRole,(session['user'],))
    if not (role):
        session['msg']="required to dispose of assets"
        return redirect(url_for('dashboard'))
    if not (role[0][0]=="Logistics Officer"):
        session['msg']="required to have the role of Logistics Officer to dispose of assets"
        return redirect(url_for('dashboard'))
    
    if request.method=='GET':
        # Get facilities
        sqlFacilities=("SELECT facility_pk, name FROM facilities")
        facilities=lostQuery(sqlFacilities, None)
        return render_template('transfer_req.html', facility_list=facilities, req_msg=session['msg'])
    if request.method=='POST':
        atag=request.form.get('tag')
        source=request.form.get('source')
        destination=request.form.get('destination')
        # Check asset tag exists
        sqlAssetExists="SELECT facility_fk FROM assets where tag=%s"
        location=lostQuery(sqlAssetExists, (atag,))
        if not (location==source):
            session['msg']="No such asset tag at that source facility"
        else:
            #Insert request into DB
            sqlUser="SELECT user_pk from users where username=%s;"
            userPk=lostQuery(sqlUser, (session['user'],))
            sqlRequest="INSERT INTO transfer_request (requester_fk, date_requested) OUTPUT  VALUES (%s, CURRENT_DATE);"
            lostQuery(sqlRequest, (userPk,))
            sqlRequestPk="SELECT currval(pg_get_serial_sequence('transfer_request', 'request_pk'));"
            requestPk=lostQuery(sqlRequestPK, (None,))
            sqlAssetPk="SELECT asset_pk from assets where tag=%s;"
            assetPk=lostQuery(sqlAssetPk, (atag,))
            sqlTransfer="INSERT INTO asset_transfers (request_fk, asset_fk, source_fk) VALUES (%s, %s, %s);"
            lostQuery(sqlTransfer, (requestPk, assetPk, source))
            session['msg']="Transfer request successfully submitted"
        return render_template('transfer_req.html', facility_list=facilities, req_msg=session['msg'])

@app.route('/approve_req', methods=['GET', 'POST'])
def approve_req():
    # Check user is a facilities officer
     sqlRole="SELECT r.title from roles as r inner join users as u on u.role_fk=r.role_pk where u.username=%s;"
    role=lostQuery(sqlRole,(session['user'],))
    if not (role):
        session['msg']="required to dispose of assets"
        return redirect(url_for('dashboard'))
    if not (role[0][0]=="Facilities Officer"):
        session['msg']="required to have the role of Facilities Officer to dispose of assets"
        return redirect(url_for('dashboard'))
    
    if request.method=='GET':
        # Check if there exists a matching request that has not yet been approved
        requestPk=request.args['request_pk']
        headers=[('Transit ID'), ('Asset Tag'), ('Source Facilitiy'), ('Destination Facility'), ('Request Date')]
        sqlRequests="SELECT tr.request_pk, a.tag, f.name, f.name, tr.date_requested FROM transfer_request as tr inner join asset_transfers as atr on tr.request_pk=atr.request_fk inner join assets as a on atr.asset_fk=a.asset_pk inner join asset_at as at on a.asset_pk=at.asset_fk inner join facilities as f on at.facility_fk=f.facility_pk where tr.request_pk=%s and (tr.approver_fk is NULL and tr.date_approved is NULL);" # My gosh it's hideous what have I done
        requestData=lostQuery(sqlRequests, (requestPk,))
        if not (requestData):
            session['msg']="No further action required"
            return redirect(url_for('dashboard'))
        session['msg']="Please review the transfer request and approve or reject it"
        return render_template('approve_req.html', approve_msg=session['msg'], requestPk=requestPk, tableheader=headers, request=requestData)
    if request.method=='POST':
        approved=request.form.get('Decision')
        requestPk=request.form.get('requestPk')
        if not (approved):
            # Remove request or mark rejecteda
            sqlReject="DELETE FROM transfer_request where request_id=%s"
            lostQuery(sqlReject, (requestPk,))
            session['msg']="Transfer request rejected"
            return redirect(url_for('dashboard'), usermsg=session['msg'])
        else:
            # Mark request approved
            # Insert asset in transit data
            sqlUser="SELECT user_pk from users where username=%s;"
            userPk=lostQuery(sqlUser, (username,))
            sqlApprove="UPDATE transfer_request set approver_fk=%s, date_approved=CURRENT_DATE;"
            lostQuery(sqlApprove, (userPk,))
            session['msg']="Transfer request approved"
            return redirect(url_for('dashboard'), usermsg=session['msg'])

@app.route('/update_transit', methods=['GET', 'POST'])
def update_transit():
    # Check if user is a logistics officer
    sqlRole="SELECT r.title from roles as r inner join users as u on u.role_fk=r.role_pk where u.username=%s;"
    role=lostQuery(sqlRole,(session['user'],))
    if not (role):
        session['msg']="required to dispose of assets"
        return redirect(url_for('dashboard'))
    if not (role[0][0]=="Logistics Officer"):
        session['msg']="required to have the role of Logistics Officer to dispose of assets"
        return redirect(url_for('dashboard'))
    
    if request.method=='GET':
        # Check if there exists a matching transit without a load/unload time
        requestPk=request.args['request_pk']
        headers=[('Transit ID'), ('Asset Tag'), ('Source Facilitiy'), ('Destination Facility'), ('Request Date')]
        sqlRequests="SELECT tr.request_pk, a.tag, f.name, f.name, tr.date_requested FROM transfer_request as tr inner join asset_transfers as atr on tr.request_pk=atr.request_fk inner join assets as a on atr.asset_fk=a.asset_pk inner join asset_at as at on a.asset_pk=at.asset_fk inner join facilities as f on at.facility_fk=f.facility_pk where tr.request_pk=%s and (tr.approver_fk is not NULL and ((atr.load is NULL or atr.unload is NULL) or (atr.load is NULL and atr.unload is NULL)));" # My gosh it's hideous what have I done
        requestData=lostQuery(sqlRequests, (requestPk,))
        if not (requestData):
            session['msg']="No further action required"
            return redirect(url_for('dashboard'))
        session['msg']="Please enter the dates to load and unload the asset"
        return render_template('update_transit.html', update_msg=session['msg'], tableheader=headers, request=requestData, request_fk=requestPk)
    if request.method=='POST':
        # Update load or unload times
        requestPk=request.form.get('submit')
        load=request.form.get('load')
        unload=request.form.get('unload')
        sqlSchedule="UPDATE asset_transfers SET load=%s, unload=%s where request_fk=%s;"
        lostQuery(sqlSchedule, (load, unload, requestPk))
        session['msg']="Transit request updated"
        return redirect(url_for('dashboard'))

@app.route('/transfer_report', methods=['GET', 'POST'])
def transfer_report():
    if request.method=='GET':
        session['msg']="Please enter the date for assets in transit"
        blank=iter([])
        return render_template('transfer_report.html', transfer_msg=session['msg'], tableheader=blank, report_list=blank)
    if request.method=='POST':
        date=request.form.get('date')
        headers=[('Asset Tag'), ('Load Time'), ('Unload Time')]
        # SELECT asset tag, load time, unload time of all assets load time <= date <= unload time
        sqlReport="SELECT a.tag, atr.load, atr.unload from asset_transfers as atr inner join assets as a on atr.asset_fk=a.asset_pk where atr.load <= %s and (atr.unload >= %s or atr.unload is NULL);"
        # If unload time is null, that's ok. If load time is null, can't determine
        report=lostQuery(sqlReport, (date, date))
        session['msg']="Report generated"
        return render_template('transfer_report.html', transfer_msg=session['msg'], tableheader=headers, report_list=report);

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Get role
    sqlRole="SELECT r.title from roles as r inner join users as u on u.role_fk=r.role_pk where u.username=%s;"
    role=lostQuery(sqlRole,(session['user'],))[0][0]
    # Get tasks appropriate to role: 
    # If Logistics Officer, add transit tracking
    if (role=="Logistics Officer"):
        headers=[('Transit ID'), ('Asset Tag'), ('Source Facilitiy'), ('Destination Facility'), ('Approval Date')]
        sqlTracking="SELECT tr.request_pk, a.tag, f.name, f.name, tr.date_approved FROM transfer_request as tr inner join asset_transfers as atr on tr.request_pk=atr.request_fk inner join assets as a on atr.asset_fk=a.asset_pk inner join asset_at as at on a.asset_pk=at.asset_fk inner join facilities as f on at.facility_fk=f.facility_pk where (atr.load is NULL or atr.unload is NULL);" # My gosh it's hideous what have I done
        todo=lostQuery(sqlRequests, (None,))

    # If Facilities Officer, approve transit requests, 
    if (role=="Facilities Officer"):
        headers=[('Transit ID'), ('Asset Tag'), ('Source Facilitiy'), ('Destination Facility'), ('Request Date')]
        sqlRequests="SELECT tr.request_pk, a.tag, f.name, f.name, tr.date_requested FROM transfer_request as tr inner join asset_transfers as atr on tr.request_pk=atr.request_fk inner join assets as a on atr.asset_fk=a.asset_pk inner join asset_at as at on a.asset_pk=at.asset_fk inner join facilities as f on at.facility_fk=f.facility_pk where (tr.approver_fk is NULL and tr.date_approved is NULL);" # My gosh it's hideous what have I done
        todo=lostQuery(sqlRequests, (None,))

    return render_template('dashboard.html', usermsg=session['msg'], tableheader=headers, todo_list=todo)

@app.route('/logout')
def logout():
    session['user']=""
    return redirect(url_for('login'))
