
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
            print(user)
            session["user"] = [user[0], user[1], 1]
            user = session.get("user")
        user_id = user[0]
        room_id = user[2]
        message_list = messages.get_messages(user_id, room_id)
        room_list = rooms.get_rooms()
        room = room_list[0][1]
        print(message_list)
        print(room_list)
        return render_template("account.html", message_list=message_list, room_list=room_list, room=room)
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
 #   if request.method == "POST":
 #       message = request.form["message"]
 #       username = request.form["username"]
 #       sql = "INSERT INTO messages (message, username, time) VALUES (:message, :username, NOW())"
 #       db.session.execute(sql, {"message":name,"username":username})
 #       db.session.commit()
 #       result = db.session.execute("SELECT message, username, time FROM messages")
 #       messages = result.fetchall()
 #,messages=messages

@app.route("/sendmessage", methods=["POST"])
def send_message():
    user = session.get("user")
    message = request.form["message"]
    messages.send_message(user, message)
    return redirect("/")

@app.route("/changeroom", methods=["POST"])
def change_room():
    room = request.form["room"]
    user = session.get("user")
    session["user"] = [user[0], user[1], room]
    return redirect("/")