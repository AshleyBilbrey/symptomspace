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
                    "name": "",
                    "email": "",
                    "affiliate": "",
                    "login_time": new_login_time,
                    "login_code": new_login_code,
                    "current_survey_id": ""
                }
                users.insert_one(newuser)
            return "Check your texts for a login code!"
    else:
        return "Error"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
   app.run()
