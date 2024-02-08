from flask import Flask, render_template, request, redirect
import flask_login

import pymysql
import pymysql.cursors
app = Flask(__name__)

app.secret_key = "ChraizardIchooseYou" #chnage this!


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True
    def __init__(self,id, username):
        
        self.username = username 
        self.id = id

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    cursor = conn.cursor()
    
    cursor.excute("SELECT * FROM 'users' WHERE 'id' =" + user_id)

    result = cursor.fetchone()

    if result is None:
         return None
    return User(result ["id", result ["username"]])




conn = pymysql.connect(
    database="jedouard_Algorithmic_Snap",
    user="jedouard",
    password="224449553",
    host="10.100.33.60",
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
        if flask_login.current_user.is_authenticated:
            return redirect ('feed')
        return render_template ("home.html.jinja")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        dob = request.form['birthday']
        username = request.form['username']
        password = request.form['password']

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO `users` (fname, lname, dob, username, password) VALUES ('{fname}', '{lname}', '{dob}', '{username}', '{password}')")
        cursor.close()
        conn.commit()
        


        

    return render_template('sign_up.html.jinja')

@app.route('/feed')
@flask_login.login_required
def feed():
    return flask_login.current_user
    return render_template('feed.html.jinja')


@app.route('/signin')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `users` WHERE username='{username}'")
        result = cursor.fetchone()
        if result and result['password'] == password:
             user = load_user(result ['id'])

             flask_login.login_user(user)
             return redirect('/feed')
        else:
            error= "Invalid username or password. Please try again."
        return render_template('login.html.jinja', error=error)
    
    return render_template('sign_in.html.jinja') 


        







 

