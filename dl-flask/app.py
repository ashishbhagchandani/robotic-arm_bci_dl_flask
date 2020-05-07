from flask import Flask, render_template, request, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from numpy import loadtxt
import numpy as np
import tensorflow as tf
import yaml

app=Flask(__name__)
Bootstrap(app)
mysql = MySQL(app)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/robotic_arm/')
def robotic_arm():
    return render_template('robotic_arm.html')

@app.route('/bci/')
def bci():
    return render_template('bci.html')

@app.route('/neural_network/')
def neural_network():
    return render_template('neural_network.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
         userDetails = request.form
         if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register.html')
         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO user(first_name, last_name, age, user_name, email, password) "\
         "VALUES(%s,%s,%s,%s,%s,%s)",(userDetails['first_name'], userDetails['last_name'], \
         userDetails['age'], userDetails['username'], userDetails['email'], userDetails['password']))
         mysql.connection.commit()
         cur.close()
         flash('Registration successful! Please login.', 'success')
         return redirect('/login')
        return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM user WHERE user_name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['firstName'] = user['first_name']
                session['lastName'] = user['last_name']
                session['userName'] = user['user_name']
                flash('Welcome ' + session['firstName'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')    
    return render_template('login.html')

@app.route('/new_check/', methods=['GET', 'POST'])
def new_check():
    if request.method == 'POST':
        bcflr = tf.keras.models.load_model('dlm.h5')
        bcflr._make_predict_function()
        
        # summarize model.
        bcflr.summary()
        
        # load dataset
        data = loadtxt(fname="checktest.csv", delimiter=",")
        
        # split into input (X) and output (Y) variables
        x= data[:,0:3]
        y= data[:,4:9]
        
        #prediction
        x1=data[:,4]                  #case5(poor quality)
        y1=np.array(x1)
        a1=np.count_nonzero(y1 == 1)
        print(a1)
        
        x2=data[:,5]                  #case1(attention with calmness)
        y2=np.array(x2)
        a2=np.count_nonzero(y2 == 1)
        print(a2)
        
        x3=data[:,6]                  #case2(No attention with calmness)
        y3=np.array(x3)
        a3=np.count_nonzero(y3 == 1)
        print(a3)
        
        x4=data[:,7]                  #case3(Attention with no calmness)
        y4=np.array(x4)
        a4=np.count_nonzero(y4 == 1)
        print(a4)
        
        x5=data[:,8]                  #case4(No attention with no calmness)
        y5=np.array(x5)
        a5=np.count_nonzero(y5 == 1)
        print(a5)
        
        if(a1>a2 and a1>a3 and a1>a4 and a1>a5):
            state="poor quality"
        elif(a2>a1 and a2>a3 and a2>a4 and a2>a5):
            print("attention with calmness")
        elif(a3>a1 and a3>a2 and a3>a4 and a3>a5):
            state="No attention with calmness"
        elif(a4>a1 and a4>a2 and a4>a3 and a4>a5):
            state="Attention with no calmness"
        else:
            state="No attention with no calmness"
        print(state)
        state_print=state
        
        # evaluate the model
        score = bcflr.evaluate(x, y, verbose=0)
        print("%s: %.2f%%" % (bcflr.metrics_names[1], score[1]*100))
        state_accuracy=score[1]*100
        
    
        
        checkup = request.form
        user_name = session['userName']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO result(state, acuracy, date_time, user_name) VALUES(%s, %s, %s, %s)", (state_print, state_accuracy, checkup['date'], user_name))
        mysql.connection.commit()
        cur.close()
        flash("Result ready", 'success')
        return render_template('new_check.html', state ='Current State of brain: {}'.format(state_print), accuracy ='Accuracy of data collected: {}%'.format(state_accuracy))    
    return render_template('new_check.html')


@app.route('/my_result/')
def my_result():
    user_name = session['userName']
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM result WHERE user_name = %s",[user_name])
    if result_value > 0:
        my_results = cur.fetchall()
        return render_template('my_results.html',my_results=my_results)
    else:
        return render_template('my_results.html',my_results=None)
    
@app.route('/result/<int:id>/')
def result(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM result WHERE result_id = {}".format(id))
    if resultValue > 0:
        result = cur.fetchone()
        return render_template('results.html', result=result)
    return 'Result not found'    

@app.route('/delete_result/<int:id>/', methods=['GET'])
def delete_result(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM result WHERE result_id = {}".format(id))
    mysql.connection.commit()
    flash("Your result has been deleted", 'success')
    return redirect('/my_result')

@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return render_template('logout.html')

if __name__=='__main__':
    app.run() 