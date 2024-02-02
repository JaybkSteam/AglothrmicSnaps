from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
from pprint import pprint as print
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

conn = pymysql.connect(
    database="jedouard_Algorithmic_Snap",
    user="jedouard",
    password="224449553",
    host="10.100.33.60",
    cursorclass=pymysql.cursors.DictCursor
)
@app.route('/')
def index():
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
        

       

        

    return render_template('signup.html.jinja')


@app.route('/signin')
def login():
    return render_template('sign_in .html.jinja')


