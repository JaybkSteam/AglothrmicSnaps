from flask import Flask, render_template, request, redirect
import flask_login
from datetime import datetime
from flask import g
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
     
    cursor = get_db().cursor()

    cursor.execute(f"(SELECT * FROM `users` WHERE `id` = {user_id}))")

    check = cursor.fetchone()

    cursor.close()

    get_db().commit()

    if check is None:
         
        return None
    
    return User(check["id"], check ["pfp"], check["email"], check["username"])

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="jedouard",
        password="224449553",
        database="jedouard_Algorithmic_Snap",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'): 
        g.db.close() 

@app.route('/')
def index():
        if flask_login.current_user.is_authenticated:
            return redirect ('feed')
        return render_template ("home.html.jinja")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        dob = request.form['birthday']
        username = request.form['username']
        password = request.form['password']

        cursor =  get_db().cursor()

        cursor.execute(f"INSERT INTO `Users` (`Username`, `Password`, `dob` ) VALUES ('{username}', '{password}', '{dob}')")
        cursor.close()
        get_db().commit
        


        

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
        cursor = get_db().commit
        cursor.execute(f"SELECT * FROM `Users` WHERE username='{username}'")
        result = cursor.fetchone()
        if result and result['password'] == password:
             user = load_user(result ['id'])

             flask_login.login_user(user)
             return redirect('/feed')
        else:
            error= "Invalid username or password. Please try again."
        return render_template('login.html.jinja', error=error)
    
    return render_template('sign_in.html.jinja')  


@app.route('/post', methods=['POST'])
@flask_login.login_required
def create_post():
    description = request.form['description']
    user_id = flask_login.current_user.id
    
    
    cursor = get_db().commit


    cursor.execute("INSERT INTO 'posts' ('description', 'user_id')")







 

