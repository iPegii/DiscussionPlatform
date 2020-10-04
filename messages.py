from app import app
import db

from flask import session, redirect, session
from os import getenv
app.secret_key = getenv("SECRET_KEY")

def send_message(user, message):
    print(user)
    if len(message) < 1:
        print('too short')
        return 'too short'
    if user[1] == None:
        print('no user')
        return 'no user'
    db.add_message(user[0], message)

def get_messages():
    return db.get_messages()