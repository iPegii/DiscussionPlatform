from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import datetime

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def check_username(username):
    sql = "SELECT COUNT(username) FROM users WHERE username=:username"
    usernameResult = db.session.execute(sql, {"username":username})
    usernameFound = usernameResult.fetchone()[0]
    if(usernameFound == 1):
        sql = "SELECT id, username FROM users WHERE username=:username"
        userResult = db.session.execute(sql, {"username":username})
        user = userResult.fetchall()[0]
        return user
    else:
        return usernameFound

def get_password(username):
    sql = "SELECT password FROM users WHERE username=:username"
    passwordResult = db.session.execute(sql, {"username":username})
    userPassword = passwordResult.fetchone()[0]
    return userPassword

def create_user(username, name, passwordHash):
    sql = "INSERT INTO users (name, username, password) VALUES (:name, :username, :password)"
    db.session.execute(sql, {"name":name,"username":username,"password":passwordHash})
    db.session.commit()

def add_message(user_id, message):
    sql = "INSERT INTO messages (message, user_id, created_at) VALUES (:message, :user_id, NOW())"
    db.session.execute(sql, {"user_id":user_id, "message":message})
    db.session.commit()

def get_messages():
    result = db.session.execute("SELECT message, username, created_at FROM messages, users WHERE messages.user_id=users.id")
    messages = result.fetchall()
    return messages