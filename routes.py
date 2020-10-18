
from app import app
import account_manager
from flask import render_template, redirect, request, session, flash
from os import getenv
import messages
import rooms
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    user = session.get("user")
    if user != None:
        if(len(user) <= 3):
            session["user"] = [user[0], user[1]]
        room_id = 1
        message_list = messages.get_messages(room_id)
        room_list = rooms.get_rooms()
        room = room_list[room_id - 1]
        user_room_list = rooms.get_user_rooms(user[0])
        return render_template("account.html", message_list=message_list, room_list=room_list, room=room, user_room_list=user_room_list)
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def page1():
    if request.method == 'POST':
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        if len(username) < 1:
            flash("Username is too short")
            return ('', 204)
        if len(password) < 8:
            flash("Password is too short")
            return ('', 204)
        if request.form['Submit'] == 'Login':
            if account_manager.login(username, password) == 'Logged in':
              #     print('Logged in ')
              #      session["username"] = username
                    flash('Logged in')
                    return redirect("/")
            else:
                flash('Username or password not correct', 'info')
        elif request.form['Submit'] == 'Register':
            register = account_manager.register(username, name, password)
            if register == 'Username is taken':
                flash('Username has been taken', 'info')
                return ('', 204)
            elif register == 'Register was succesful!':
                flash('Register was succesful!')
                return ('', 204)
        else:
            print('No idea.')
    elif request.method == "GET":
        if session.get("user") != None:
            return redirect("/")
    return render_template("login.html")

@app.route("/account", methods=["POST", "GET"])
def account():
    if session.get("user") != None:
        return render_template("account.html")
    else:
        return redirect("/login")

@app.route("/sendmessage", methods=["POST"])
def send_message():
    user = session.get("user")
    message = request.form["message"]
    room_id = request.form["room"]
    messages.send_message(user, message, room_id)
    return redirect("/")

@app.route("/rooms/<int:id>", methods=["GET"])
def change_room(id):
    user_id = session.get("user")[0]
    message_list = messages.get_messages(id)
    room_list = rooms.get_rooms()
    user_room_list = rooms.get_user_rooms(user_id)
    return render_template("account.html", message_list=message_list, room_list=room_list, room=id, user_room_list=user_room_list)

@app.route("/joinroom", methods=["GET"])
def join_room():
    room_id = 1
    room_name = "Amazing group"
    room_list = rooms.get_rooms()
    user_id = session.get("user")[0]
    user_room_list = rooms.get_user_rooms(user_id)
    return render_template("join.html", room_name=room_name, room_id=room_id, room_list=room_list, user_room_list=user_room_list)