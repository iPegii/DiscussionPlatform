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
        sql = "INSERT INTO users (name, username, password) VALUES (:name, :username, :password) RETURNING id"
        result = db.session.execute(sql, {"name":name,"username":username,"password":passwordHash})
        user_id = result.fetchone()[0]
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Error: creating user"

    ## Adding user to public room

    try:
        sql = "INSERT INTO rooms_users (room_id, user_id, rights) VALUES (1, :user_id, 1)"
        db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Error: adding user to public room"




def add_message(user_id, message, room_id):
    ## add message
    try: 
        sql = "INSERT INTO messages (message, user_id, created_at) VALUES (:message, :user_id, NOW()) RETURNING id"
        result = db.session.execute(sql, {"user_id":user_id, "message":message})
        message_id = result.fetchone()[0]
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Error: adding user"

    ## connect message with room_messages
    try: 
        sql = "INSERT INTO room_messages (room_id, message_id) VALUES (:r_id, :m_id)"
        db.session.execute(sql, {"r_id":room_id, "m_id":message_id})
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Error: adding user"

def get_messages(room_id):
    try:
        sql = ("SELECT M.message, M.created_at, U.name FROM messages M, users U, rooms_users RU ,room_messages RM" + 
        " WHERE RM.room_id=:room_id AND RM.message_id = M.id AND RU.room_id=:room_id AND RU.user_id = U.id AND U.id = M.user_id")
        result = db.session.execute(sql, {"room_id":room_id})
        messages = result.fetchall()
        print("db:", messages)
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

def get_user_rooms(user_id):
    try:
        sql = "SELECT R.id, R.room_name FROM rooms R, rooms_users RU WHERE RU.room_id = R.id AND RU.user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        rooms = result.fetchall()
        return rooms
    except IntegrityError:
        db.session.rollback()
        return "Error: fetching user rooms"