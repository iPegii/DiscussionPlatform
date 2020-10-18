from app import app
import db


def get_rooms():
    return db.get_rooms()