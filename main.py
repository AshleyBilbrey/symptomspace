from flask import Flask, request, render_template, session, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import re
import time
from time import gmtime, strftime
import random
import string
mongoclient = MongoClient()
db = mongoclient.symptomspace_database
app = Flask(__name__)

@app.route("/")
def serve_index():
    return render_template('index.html')

@app.route("/login", methods = ["POST", "GET"])
def serve_login():
    if request.method == "GET":
        if 'session_id' in session:
            return redirect(url_for('serve_dashboard'))
        else:
            if request.args.get("status") == '1':
                msg = "Your login session has expired."
                return render_template('login.html', message = msg)
            elif request.args.get("status") == '2':
                msg = "That's not a valid login code!"
                return render_template('login2.html', phone_number = request.args.get("phone-number"), message = msg)
            else:
                return render_template('login.html')
    elif request.method == "POST":
        #Check if valid phone number
        phonenumber = request.form["phone-number"]
        search = re.search("[0-9]{10}", phonenumber)
        if search == None:
            return "That's not a valid phone number!"
        else:
            #Check if user exists
            users = db.users
            user = users.find_one({"phone_number": phonenumber})
            new_login_time = time.time()
            new_login_code = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(15))
            if user != None:
                user["login_time"] = new_login_time
                user["login_code"] = new_login_code
                user_id = user['_id']
                users.replace_one({'_id': ObjectId(user_id)}, user)
            else:
                newuser = {
                    "phone_number": phonenumber,
                    "completed_profile": False,
                    "name": None,
                    "email": None,
                    "affiliate": None,
                    "login_time": new_login_time,
                    "login_code": new_login_code,
                    "current_survey_id": None,
                    "session_id": None
                }
                users.insert_one(newuser)
            print("Send text for " + phonenumber + " with code " + new_login_code)
            return render_template("login2.html", phone_number = phonenumber)
    else:
        return "Error"

@app.route("/auth")
def auth():
    phonenumber = request.args.get('phone-number')
    verifycode = request.args.get('verify-code')
    search = re.search("[0-9]{10}", phonenumber)
    if(search == None):
        return "There was an error processing your request."
    else:
        users = db.users
        user = users.find_one({"phone_number": phonenumber})
        if(user == None):
            return redirect("/login?status=2&phone-number=" + phonenumber)
        else:
            if time.time() > (user["login_time"] + 600):
                return redirect("/login?status=1")
            elif verifycode != user["login_code"]:
                return redirect("/login?status=2&phone-number=" + phonenumber)
            elif user["login_code"] == None:
                return redirect("/login?status=2&phone-number=" + phonenumber)
            else:
                new_session_id = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
                user["session_id"] = new_session_id
                user["login_code"] = None
                session['session_id'] = new_session_id
                user_id = user['_id']
                users.replace_one({'_id': ObjectId(user_id)}, user)
                return redirect(url_for('serve_dashboard'))

@app.route("/logout")
def logout():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        #If they logout without a valid session ID
        if user == None:
            session.pop("session_id", None)
            return "There was an error processing your request."
        else:
            user["session_id"] = None
            user_id = user['_id']
            users.replace_one({'_id': ObjectId(user_id)}, user)
            session.pop("session_id", None)
            return redirect(url_for('serve_index'))
    else:
        return "There was an error processing your request."

@app.route("/dashboard")
def serve_dashboard():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["completed_profile"] == False:
            return render_template("incomplete_profile.html")
        else:
            #Check if they have a valid survey, if they do, serve it.
            cali_time = time.time() - 28800
            cali_date = strftime("%Y-%m-%d", gmtime(cali_time))
            surveys = db.surveys
            most_recent_time = 0
            user_current_survey_id = user["current_survey_id"]
            if user["current_survey_id"] == None:
                return render_template("dashboard.html", name = user["name"])
            else:
                user_current_survey = surveys.find_one({"_id": user_current_survey_id})
                if user_current_survey["day"] != cali_date:
                    return render_template("dashboard.html", name = user["name"])
                elif user_current_survey["approved"] == True:
                    return render_template("user_approved_survey.html", name = user["name"])
                elif user_current_survey["approved"] == False:
                    return render_template("user_unapproved_survey.html", name = user["name"])
                else:
                    return "There was an error processing your request."
    else:
        return redirect(url_for("serve_login"))

@app.route("/user/update", methods = ["POST", "GET"])
def user_update():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
    if request.method == "POST":
        user["name"] = request.form["full-name"]
        user["email"] = request.form["email"]
        user["affiliate"] = request.form["af-status"]
        user["completed_profile"] = True
        user_id = user['_id']
        users.replace_one({'_id': ObjectId(user_id)}, user)
        return redirect(url_for("serve_dashboard"))
    elif request.method == "GET":
        return render_template("user_update.html")
    else:
        return "There was an error processing your request."


#Delete this later!
@app.route("/tempbase")
def temp_base():
    return render_template("base.html")

@app.route("/survey", methods = ["GET", "POST"])
def serve_survey_page():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
    if request.method == "GET":
        return render_template("survey.html")
    elif request.method == "POST":
        print(request.form)
        approved = True
        if request.form["flu"] != "yes":
            print("No flu test")
            approved = False
        if request.form["covid-test"] == "no":
            print("No covid test")
            approved = False
        if request.form["symptoms"] != "NONE":
            print("Symptoms nono")
            approved = False
        if request.form["positive"] != "no":
            print("Positive test")
            approved = False
        if request.form["close-contact"] != "no":
            print("In close contact")
            approved = False
        if request.form["certify"] == None:
            print("Not true")
            approved = False

        cali_time = time.time() - 28800
        new_survey = {
            "user_id": user["_id"],
            "time": cali_time,
            "day": strftime("%Y-%m-%d" , gmtime(cali_time)),
            "approved": approved
        }
        survey_id = db.surveys.insert_one(new_survey).inserted_id
        user["current_survey_id"] = survey_id
        user_id = user['_id']
        users.replace_one({'_id': ObjectId(user_id)}, user)
        return redirect(url_for("serve_dashboard"))

    else:
        return "There was an error processing your request."

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    f = open("./secrets/secret_key.txt", "r")
    print("SECRET KEY SHH: " + f.read(25))
    app.secret_key = f.read(25)
    app.run()
