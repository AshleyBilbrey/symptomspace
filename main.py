from flask import Flask, request, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import re
import time
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
            return redirect(url_for('dashboard'))
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
            return "Check your texts for a login code!"
    else:
        return "Error"

@app.route("/auth")
def auth():

    phonenumber = request.form["phone-number"]
    verifycode = request.form["verify-code"]
    search = re.search("[0-9]{10}", phonenumber)
    if(search == None):
        return "There was an error processing your request."
    else:
        users = db.users
        user = users.find_one({"phone_number": phonenumber})
        if(user == None):
            return "That's not a valid login code!"
        else:
            if time.time() > (user["login_time"] + 600):
                return "Your login session has expired."
            elif verifycode != user["login_code"]:
                return "That's not a valid login code!"
            else:
                new_session_id = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
                user["session_id"] = new_session_id
                session['session_id'] = new_session_id
                user_id = user['_id']
                users.replace_one({'_id': ObjectId(user_id)}, user)
                return redirect(url_for('dashboard'))

@app.route("/logout")
    users = db.users
    user = user.find_one({"session_id", session["session_id"]})
    if user == None:
        session.pop("session_id", None)
        return "There was an error processing your request"
    else:
        user["session_id"] = None
        user_id = user['_id']
        users.replace_one({'_id': ObjectId(user_id)}, user)
        session.pop("session_id", None)
        return redirect(url_for('index'))



#Delete this later!
@app.route("/tempbase")
def temp_base():
    return render_template("base.html")

@app.route("/survey")
def serve_survey_page():
    return render_template("survey.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
   app.run()
   f = open("/secrets/secret_key.txt", "r")
   app.secret_key = f.read(25)
