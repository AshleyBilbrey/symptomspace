from flask import Flask, request, render_template, session, redirect, url_for, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
import re
import time
from time import gmtime, strftime
import random
import string
import qrcode
import io
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
                    "session_id": None,
                    "scanner_perm": False,
                    "admin_perm": False
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
        return "There was an error processing your request. You may have been logged in from another location."
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
            return "There was an error processing your request. You may have been logged in from another location."
        else:
            user["session_id"] = None
            user_id = user['_id']
            users.replace_one({'_id': ObjectId(user_id)}, user)
            session.pop("session_id", None)
            return redirect(url_for('serve_index'))
    else:
        return "There was an error processing your request. You may have been logged in from another location."

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
                    return render_template("user_approved_survey.html", name = user["name"], survey_id = user_current_survey_id, date = cali_date)
                elif user_current_survey["approved"] == False:
                    return render_template("user_unapproved_survey.html", name = user["name"], survey_id = user_current_survey_id, date = cali_date)
                else:
                    return "There was an error processing your request. You may have been logged in from another location."
    else:
        return redirect(url_for("serve_login"))

@app.route("/user/")
def user_info():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        return render_template("user_info.html", phonenumber = user["phone_number"], name = user["name"], email = user["email"], affiliate = user["affiliate"], scanner = user["scanner_perm"], admin = user["admin_perm"])
    else:
        return redirect(url_for("serve_login"))

@app.route("/user/<phone_number>")
def other_user(phone_number):
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["admin_perm"] != True:
            return "Unauthorized"
        else:
            user2 = users.find_one({"phone_number": phone_number})
            return render_template("user_info.html", phonenumber = user2["phone_number"], name = user2["name"], email = user2["email"], affiliate = user2["affiliate"], status = 1, scanner = user2["scanner_perm"], admin = user2["admin_perm"])
    else:
        return redirect(url_for("serve_login"))

@app.route("/user/all")
def user_all():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["admin_perm"] != True:
            return "Unauthorized"
        else:
            names = []
            numbers = []
            for u in users.find():
                names.append(u["name"])
                numbers.append(u["phone_number"])
            return render_template("all_users.html", names = names, numbers = numbers, r = users.find().count())
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
            return redirect(url_for("user_info"))
        elif request.method == "GET":
            return render_template("user_update.html", email = user["email"], name = user["name"], affiliate = user["affiliate"])
        else:
            return "There was an error processing your request. You may have been logged in from another location."
    else:
        return redirect(url_for("serve_login"))

@app.route("/user/update/<phone_number>", methods = ["GET", "POST"])
def edit_other_user(phone_number):
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["admin_perm"] != True:
            return "Unauthorized"
        else:
            user2 = users.find_one({"phone_number": phone_number})
            if request.method == "GET":
                return render_template("user_update_other.html", phonenumber = phone_number, email = user2["email"], name = user2["name"], affiliate = user2["affiliate"], scanner = user2["scanner_perm"], admin = user2["admin_perm"])
            elif request.method == "POST":
                user2["name"] = request.form["full-name"]
                user2["email"] = request.form["email"]
                user2["affiliate"] = request.form["af-status"]

                if request.form.get("is-scanner") == "yes":
                    user2["scanner_perm"] = True
                else:
                    user2["scanner_perm"] = False

                if request.form.get("is-admin") == "yes":
                    user2["admin_perm"] = True
                else:
                    user2["admin_perm"] = False

                print(user2)

                db.users.replace_one({"phone_number": phone_number}, user2)

                return redirect("/user/" + phone_number)
            else:
                return "There was an error processing your request. You may have been logged in from another location."
    else:
        return redirect(url_for("serve_login"))

@app.route("/qr/<code>")
def make_qr(code):
    img_IO = io.BytesIO()
    qrcode.make(code).save(img_IO, 'png')
    img_IO.seek(0)
    return send_file(img_IO, mimetype='image/png')


#Delete this later!
@app.route("/tempbase")
def temp_base():
    return render_template("scan_neutral.html")

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
        try:
            if request.form["flu"] != "yes":
                approved = False
            if request.form["covid-test"] == "no":
                approved = False
            if request.form["symptoms"] != "NONE":
                approved = False
            if request.form["positive"] != "no":
                approved = False
            if request.form["close-contact"] != "no":
                approved = False
            if request.form["certify"] == None:
                approved = False
        except:
            return render_template("survey.html", status = 1)

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
        return "There was an error processing your request. You may have been logged in from another location."

@app.route("/location/")
def all_locations():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["admin_perm"] != True:
            return "Unauthorized"
        else:
            locations = db.locations
            loc_names = []
            loc_ids = []
            for loc in locations.find():
                loc_names.append(loc["name"])
                loc_ids.append(loc["_id"])
            return render_template("all_locations.html", loc_names = loc_names, loc_ids = loc_ids, r = locations.find().count())
    else:
        return redirect(url_for("serve_login"))

@app.route("/location/add", methods = ["GET", "POST"])
def add_location():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["admin_perm"] != True:
            return "Unauthorized"
        else:
            if request.method == "GET":
                return render_template("add_location.html")
            elif request.method == "POST":
                locations = db.locations
                new_loc = {
                    "name": request.form["loc-name"],
                    "address": request.form["loc-address"]
                }
                locations.insert_one(new_loc)
                return redirect(url_for("all_locations"))
            else:
                return "There was an error processing your request. You may have been logged in from another location."
    else:
        return redirect(url_for("serve_login"))

@app.route("/location/<loc_id>")
def location_info(loc_id):
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["admin_perm"] != True:
            return "Unauthorized"
        else:
            locations = db.locations
            location = locations.find_one({"_id": ObjectId(loc_id)})
            return render_template("location_info.html", id = loc_id, name = location["name"], address = location["address"])
    else:
        return redirect(url_for("serve_login"))

@app.route("/location/update/<loc_id>", methods = ["GET", "POST"])
def update_location(loc_id):
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["admin_perm"] != True:
            return "Unauthorized"
        else:
            locations = db.locations
            location = locations.find_one({"_id": ObjectId(loc_id)})
            if request.method == "GET":
                return render_template("location_update.html", id = loc_id, name = location["name"], address = location["address"])
            elif request.method == "POST":
                location["name"] = request.form["loc-name"]
                location["address"] = request.form["loc-address"]
                locations.replace_one({"_id": ObjectId(loc_id)}, location)
                return redirect("/location/" + loc_id)
            else:
                return "There was an error processing your request. You may have been logged in from another location."
    else:
        return redirect(url_for("serve_login"))

@app.route("/scan")
def start_scan():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["scanner_perm"] != True:
            return "Unauthorized"
        else:
            locations = db.locations
            loc_names = []
            loc_ids = []
            for loc in locations.find():
                loc_names.append(loc["name"])
                loc_ids.append(loc["_id"])
            return render_template("start_scanning.html", loc_names = loc_names, loc_ids = loc_ids, r = locations.find().count())
    else:
        return redirect(url_for("serve_login"))

@app.route("/scan/<loc_id>")
def scan(loc_id):
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["scanner_perm"] != True:
            return "Unauthorized"
        else:
            locations = db.locations
            location = locations.find_one({"_id": ObjectId(loc_id)})
            loc_name = location["name"]
            return render_template("scan_neutral.html", loc_name = loc_name, loc_id = loc_id, time = time.time())
    else:
        return redirect(url_for("serve_login"))

@app.route("/verify")
def verify():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["scanner_perm"] != True:
            return "Unauthorized"
        else:
            check = True
            cali_time = time.time() - 28800
            survey_id = request.args.get("survey_id")
            loc_id = request.args.get("loc_id")
            surveys = db.surveys
            survey = surveys.find_one({"_id": ObjectId(survey_id)})
            survey_user_id = survey["user_id"]
            survey_user = users.find_one({"_id": survey_user_id})
            if survey["_id"] != survey_user["current_survey_id"]:
                check = False
            elif survey["approved"] == False:
                check = False
            elif survey["day"] != strftime("%Y-%m-%d" , gmtime(cali_time)):
                check = False

            checkins = db.checkins
            newcheckin = {
                "loc_id": ObjectId(loc_id),
                "user_id": survey_user_id,
                "time": cali_time,
                "day": strftime("%Y-%m-%d" , gmtime(cali_time)),
                "result": check,
                "retroactive_check": check
            }
            checkins.insert_one(newcheckin)
            response = {
                "name": survey_user["name"],
                "check": check
            }
            return response
    else:
        return redirect(url_for("serve_login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    f = open("./secrets/secret_key.txt", "r")
    print("SECRET KEY SHH: " + f.read(25))
    app.secret_key = f.read(25)
    app.run()
