from app import app
import db

def send_message(user, message):
    if len(message) < 1:
        print('too short')
        return 'too short'
    if user[1] == None:
        print('no user')
        return 'no user'
    db.add_message(user[0], message)

def get_messages(user_id, room_id):
    return db.get_messages(user_id, room_id)