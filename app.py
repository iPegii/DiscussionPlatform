from flask import Flask
from flask import render_template, request, redirect, session, flash
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
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        if request.form['Submit'] == 'Login':
            print('Login it is')
            passwordHash = generate_password_hash(password)
            sql = "SELECT COUNT(username) FROM users WHERE username=:username"
            usernameResult = db.session.execute(sql, {"username":username})
            isUsername = usernameResult.fetchone()[0]
            if isUsername == 1:
                sql = "SELECT password FROM users WHERE username=:username"
                passwordResult = db.session.execute(sql, {"username":username})
                actualPassword = passwordResult.fetchone()[0]
                if check_password_hash(actualPassword, password):
                    print('Logged in ')
                    session["username"] = username
                    flash('Logged in')
                    return redirect("/frontpage")
                else: 
                    flash('Username or password not correct')
            else:
                pass
                flash('Username or password not correct')
        elif request.form['Submit'] == 'Register':
            print('Register it is')
            passwordHash = generate_password_hash(password)
            sql = "SELECT COUNT(username) FROM users WHERE username=:username"
            usernameResult = db.session.execute(sql, {"username":username})
            isUsername = usernameResult.fetchone()[0]
            if isUsername == 1:
                flash('Username has been taken')
            else:
                sql = "INSERT INTO users (name, username, password) VALUES (:name, :username, :password)"
                db.session.execute(sql, {"name":name,"username":username,"password":passwordHash})
                db.session.commit()
                flash('Register was succesful!')
        else:
            print('No idea.')
    return render_template("register.html")

@app.route("/frontpage", methods=["POST", "GET"])
def frontpage():
 #   if request.method == "POST":
 #       message = request.form["message"]
 #       username = request.form["username"]
 #       sql = "INSERT INTO messages (message, username, time) VALUES (:message, :username, NOW())"
 #       db.session.execute(sql, {"message":name,"username":username})
 #       db.session.commit()
 #       result = db.session.execute("SELECT message, username, time FROM messages")
 #       messages = result.fetchall()
 #,messages=messages
    return render_template("frontpage.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    del session["username"]
    return redirect("/")