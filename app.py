from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def page1():
    if request.method == 'POST':
        if request.form['Submit'] == 'Login':
            print('Login it is')
            username = request.form["username"]
            password = request.form["password"]
            passwordHash = generate_password_hash(password)
            sql = "SELECT COUNT(username) FROM users WHERE username=:username"
            usernameResult = db.session.execute(sql, {"username":username})
            isUsername = usernameResult.fetchone()[0]
            if isUsername == 1:
                sql = "SELECT password FROM users WHERE username=:username"
                passwordResult = db.session.execute(sql, {"username":username})
                countPassword = passwordResult.fetchone()[0]
            else:
                print('Wrong!')
                ## Notify user of username or password being wrong
        elif request.form['Submit'] == 'Register':
            print('Register it is')
            username = request.form["username"]
            password = request.form["password"]
            passwordHash = generate_password_hash(password)
            sql = "SELECT COUNT(username) FROM users WHERE username=:username"
            usernameResult = db.session.execute(sql, {"username":username})
            isUsername = usernameResult.fetchone()[0]
            if isUsername == 1:
                pass
                ## Notify user that username is already taken
            else:
                sql = "INSERT INTO users (name, username, password) VALUES (:name, :username, :password)"
                db.session.execute(sql, {"name":name,"username":username,"password":passwordHash})
                db.session.commit()
        else:
            print('Wtf is is')
        return render_template("login.html", 
        username = username,
        password = passwordHash)

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"