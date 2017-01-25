from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from picklesession import PickleSessionInterface
import os

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


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/reportfilter', methods=['GET', 'POST'])
def reportfilter():
    facilities=['']
    convoys=['']
    uname=''
    sqlFacilities="SELECT facility_pk, common_name from facilities;"
    sqlConvoys="SELECT convoy_pk, request from convoys;"
    facilities=lostQuery(sqlFacilities)
    convoys=lostQuery(sqlConvoys)

    if request.method=='POST':
        session['user']=request.form.get('username')
        session['password']=request.form.get('password')
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('reportfilter.html', facilities_list=facilities, convoys_list=convoys, uname=session['user'])

@app.route('/report', methods=['GET', 'POST'])
def genReport(): #, asset):
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method=='POST': # and 'report' in request.form:
        reportType=request.form.get('report')
        assetAt=request.form.get('facilities')
        assetOn=request.form.get('convoys')
        session['reportType']=reportType
        session['assetAt']=assetAt
        session['assetOn']=assetOn
    if 'reportType' in session:
        #return render_template('report.html', assetAt=session['assetAt'], assetOn=session['assetOn'], rType=session['reportType'])
        reportType=session['reportType']
    else:
        reportType='reportfilter'
    return redirect(url_for(reportType))

@app.route('/facilityreport')
def facilityreport():
    if 'user' not in session:
        return redirect(url_for('login'))
    facility_fk=session['assetAt']
#    sqlFacility="SELECT facility_pk from facilities where common_name='"+facility+"';"
#    facility_fk=lostQuery(sqlFacility)
    sqlAssets="SELECT assets.asset_tag, asset_at.arrive_dt, asset_at.depart_dt from assets join asset_at on assets.asset_pk=asset_at.asset_fk where facility_fk='"+facility_fk+"';"
    assets=lostQuery(sqlAssets)
    return render_template('facilityreport.html', asset_list=assets, uname=session['user'])

@app.route('/transitreport')
def transitreport():
    if 'user' not in session:
        return redirect(url_for('login'))
    convoy_fk=str(session['assetOn'])
    sqlAssets="select a.asset_tag, ao.load_dt, f1.common_name, ao.unload_dt, f2.common_name from assets as a inner join asset_on as ao on a.asset_pk=ao.asset_fk inner join convoys as c on ao.convoy_fk=c.convoy_pk inner join facilities as f1 on c.source_fk=f1.facility_pk inner join facilities as f2 on c.dest_fk=f2.facility_pk where ao.convoy_fk='"+convoy_fk+"';"
    assets=lostQuery(sqlAssets)
    return render_template('transitreport.html', asset_list=assets, uname=session['user'])

@app.route('/logout')
def logout():
    if 'user' not in session:
        return redirect(url_for('login'))
    #if request.method=='POST':
    goodbye=session['user']
    SECRET_KEY = 'a0z987asdf'+session['user']
    app.secret_key = SECRET_KEY
    session.pop('password', None)
    session.pop('user', None)
    session.clear()
    session.modified=True
    return render_template('logout.html', uname=goodbye)
