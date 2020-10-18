from app import app
import db

def send_message(user, message, room_id):
    if len(message) < 1:
        print('too short')
        return 'too short'
    if user[1] == None:
        print('no user')
        return 'no user'
    if room_id == None:
        print('no room')
        return 'no room'
    db.add_message(user[0], message, room_id)

def get_messages(room_id):
    return db.get_messages(room_id)