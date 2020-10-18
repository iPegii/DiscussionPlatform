from app import app
import db

def get_rooms():
    return db.get_rooms()

def get_user_rooms(user_id):
    return db.get_user_rooms(user_id)