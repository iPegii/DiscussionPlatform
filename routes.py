
from app import app
import account_manager
from flask import render_template, redirect, request, session, flash
from os import getenv
import messages
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    print(session.get("user"))
    message_list = messages.get_messages()
    if session.get("user") != None:
        return render_template("account.html", messages_list=message_list)
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def page1():
    if request.method == 'POST':
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(name)
        print(password)
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
                    return render_template("account.html")
            else:
                flash('Username or password not correct', 'info')
        elif request.form['Submit'] == 'Register':
            register = account_manager.register(username, name, password)
            if register == 'Username is taken':
                flash('Username has been taken', 'info')
            elif register == 'Register was succesful!':
                flash('Register was succesful!')
        else:
            print('No idea.')
    elif request.method == "GET":
        if session.get("user") != None:
            return render_template("account.html")
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