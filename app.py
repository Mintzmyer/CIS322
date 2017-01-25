from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login')
def login():
    if request.method=='GET' and 'username' and 'login' in request.args:
        return render_template('welcome.html', user=request.args.get('username'), password=request.args.get('password'))

    if request.method=='POST' and 'username' and 'login' in request.form:
        return render_template('welcome.html', user=request.form['username'])
    return render_template('login.html')

@app.route('/reportfilter', methods=['GET', 'POST'])
def reportfilter():
    facilities=['']
    convoys=['']
    sqlFacilities="SELECT common_name from facilities;"
    sqlConvoys="SELECT request from convoys"
    facilities=lostQuery(sqlFacilities)
    convoys=lostQuery(sqlConvoys)
#    if request.method=='GET' and 'report' and 'assetIn' in request.form:
#        return render_template('index.html', report=request.args.get('report'), assetsIn=request.args.get('assetIn'))
#    if request.method=='GET' in request.form:
#        reportType='facilityreport'
#        report=request.args.get['report']
#        return redirect(url_for('genReport', reportType=report)) #, asset=assetsIn))

    if request.method=='POST': # and 'report' in request.form:
        if form.validate() == True:
            reportType=request.form['report']
            session['reportType']=reportType
            return redirect(url_for('genReport', reportType=reportType)) #, asset=assetsIn))
        else:
            return render_template('reportfilter.html')
       # assetsIn=request.form['assetIn']
    return render_template('reportfilter.html')

@app.route('/report', methods=['GET', 'POST'])
def genReport(): #, asset):
    reportType=session['reportType']
    #reportType=request.args['reportType']
    return render_template('facilityreport.html')
    #return render_template(url_for(reportType))

@app.route('/facilityreport')
def facilityreport():
    return render_template('facilityreport.html')

@app.route('/transitreport')
def transitreport():
    redir='logout'
    return render_template('transitreport.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

