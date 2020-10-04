from app import app
import db
from werkzeug.security import check_password_hash, generate_password_hash

from flask import session, redirect
from os import getenv
app.secret_key = getenv("SECRET_KEY")


def login(username, password):
    usernameFound = db.check_username(username)
    if usernameFound == 0:
        return('Username or password is not correct')
    else:
        userPassword = db.get_password(username)
        if check_password_hash(userPassword, password):
            print(usernameFound)
            user = [usernameFound[0], usernameFound[1]]
            session["user"] = user
            print('Logged in')
            return('Logged in')
        else: 
            return('Username or password is not correct')

def register(username, name, password):
    if username < 1:
        return("Username is too short")
    if password < 8:
        return("Password is too short")
    usernameFound = db.check_username(username)
    if usernameFound == 1:
        return('Username is taken')
    else:
        passwordHash = generate_password_hash(password)
        db.create_user(username, name, passwordHash)
        return('Register was succesful!')

@app.route("/logout", methods=["POST"])
def logout():
    del session["user"]
    return redirect("/")