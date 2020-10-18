from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import datetime
from sqlalchemy.exc import IntegrityError

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

    ## Creating user
    try:
        sql = "INSERT INTO users (name, username, password) VALUES (:name, :username, :password)"
        db.session.execute(sql, {"name":name,"username":username,"password":passwordHash})
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Error: creating user"

    ## Adding user to public room
    try:
        sql = "SELECT id FROM users WHERE username=:username"
        idResult = db.session.execute(sql, {"username":username}).fetchone()[0]
    except IntegrityError:
        db.session.rollback()
        return "Error: finding new user id"

    try:
        sql = "INSERT INTO (room_id, user_id, rights) VALUES (1, :user_id, 1)"
        db.session.execute(sql, {"user_id":idResult})
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Error: adding user to public room"




def add_message(user_id, message):
    try: 
        sql = "INSERT INTO messages (message, user_id, created_at) VALUES (:message, :user_id, NOW())"
        db.session.execute(sql, {"user_id":user_id, "message":message})
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Error: adding user"

def get_messages(user_id, room_id):
    try:
        sql = ("SELECT M.id, R.room_name, M.message, M.created_at, U.name FROM messages M, users U, rooms R, rooms_users RU, room_messages RM" + 
        " WHERE U.id=:user_id AND U.id = RU.user_id AND RU.room_id = RM.room_id AND RM.message_id = M.id AND RM.room_id=:room_id")
        result = db.session.execute(sql, {"user_id":user_id, "room_id":room_id})
        messages = result.fetchall()
        return messages
    except IntegrityError:
        return "Error: fetching messages"


def get_rooms():
    try:
        sql = "SELECT id, room_name FROM rooms"
        result = db.session.execute(sql)
        rooms = result.fetchall()
        return rooms
    except IntegrityError:
        db.session.rollback()
        return "Error: fetching rooms"