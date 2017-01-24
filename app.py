from flask import Flask, render_template, request

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

@app.route('/reportfilter')
def reportfilter():
    if request.method=='GET' and 'report' and 'assetIn' in request.form:
        return render_template('index.html', report=request.args.get('report'), assetsIn=request.args.get('assetIn'))

    if request.method=='POST' and 'report' and 'assetIn' in request.form:
        return render_template('index.html', report=request.form['report'], assetsIn=request.form['assetIn'])
    return render_template('reportfilter.html')


#@app.route('/goodbye')
#def goodbye();
#    if request.method=='GET' and 'mytext' in request.args:
#        return render_template('goodbye.html', data=request.args.get('mytext'))
#
#    if request.method=='POST' and 'mytext' in request.form:
#        return render_template('goodbye.html',data=request.form['mytext'])
#    return render_template('index.html')
