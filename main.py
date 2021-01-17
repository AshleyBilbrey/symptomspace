from flask import Flask, request, render_template, session, redirect, url_for, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
from twilio.rest import Client
from datetime import datetime
import googlemaps
import re
import os
import time
from time import gmtime, strftime
import random
import string
import qrcode
import io
import pprint
mongoclient = MongoClient()
db = mongoclient.symptomspace_database
app = Flask(__name__)

gmaps = googlemaps.Client(key='AIzaSyCBs-ifKG9HEbGN2i3ZbGWV_N4N8waXtec')
twilio_client = Client(open("./secrets/twilio_sid.txt", "r").read(34), open("./secrets/twilio_secret.txt", "r").read(32))

@app.route("/")
def serve_index():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user != None:
            user_is_scanner = user["scanner_perm"]
            user_is_admin = user["admin_perm"]
            logged_in = True
        else:
            user_is_scanner = False
            user_is_admin = False
            logged_in = False
    else:
        user_is_scanner = False
        user_is_admin = False
        logged_in = False
    return render_template('index.html', active = "home", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)

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
                    "admin_perm": False,
                    "exposures": []
                }
                users.insert_one(newuser)
            print("Send text for " + phonenumber + " with code " + new_login_code)
            enable_twilio = False
            if(enable_twilio):
                try:
                    message = twilio_client.messages.create(
                        body='Hello from symptom.space! Please use code ' + new_login_code + ' to log in! Or use link http://localhost:5000/auth?phone-number=' + phonenumber + '&verify-code=' + new_login_code + " Please do not share this code with anyone.",
                        from_='+16504494733',
                        to='+1' + phonenumber
                    )
                except:
                    return "We're sorry, there was an issue sending a code to that phone number. Please try again."
                print(message.sid)
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
                user_is_scanner = user["scanner_perm"]
                user_is_admin = user["admin_perm"]
                logged_in = True
                return render_template("dashboard.html", name = user["name"], active = "dashboard", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
            else:
                user_current_survey = surveys.find_one({"_id": user_current_survey_id})
                if user_current_survey["day"] != cali_date:
                    user_is_scanner = user["scanner_perm"]
                    user_is_admin = user["admin_perm"]
                    logged_in = True
                    return render_template("dashboard.html", name = user["name"], active = "dashboard", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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
        user_is_scanner = user["scanner_perm"]
        user_is_admin = user["admin_perm"]
        logged_in = True
        return render_template("user_info.html", phonenumber = user["phone_number"], name = user["name"], email = user["email"], exposures = user["exposures"], affiliate = user["affiliate"], scanner = user["scanner_perm"], admin = user["admin_perm"], active = "profile", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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
            user_is_scanner = user["scanner_perm"]
            user_is_admin = user["admin_perm"]
            logged_in = True
            return render_template("user_info.html", phonenumber = user2["phone_number"], name = user2["name"], email = user2["email"], exposures = user2["exposures"], affiliate = user2["affiliate"], status = 1, scanner = user2["scanner_perm"], admin = user2["admin_perm"], active = "users", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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
            user_is_scanner = user["scanner_perm"]
            user_is_admin = user["admin_perm"]
            logged_in = True
            return render_template("all_users.html", names = names, numbers = numbers, r = users.find().count(), active = "users", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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


@app.route("/survey", methods = ["GET", "POST"])
def serve_survey_page():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
    if request.method == "GET":
        user_is_scanner = user["scanner_perm"]
        user_is_admin = user["admin_perm"]
        logged_in = True
        return render_template("survey.html", active = "survey", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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
            user_is_scanner = user["scanner_perm"]
            user_is_admin = user["admin_perm"]
            logged_in = True
            return render_template("all_locations.html", loc_names = loc_names, loc_ids = loc_ids, r = locations.find().count(), active = "locations", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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
            user_is_scanner = user["scanner_perm"]
            user_is_admin = user["admin_perm"]
            logged_in = True
            scan_counter = 0
            problem_counter = 0
            cali_time = time.time() - 28800
            fortnite = cali_time - 1209600
            for scan in db.checkins.find({"loc_id": ObjectId(loc_id), "time": {"$gt": fortnite}}):
                scan_counter = scan_counter + 1
                if scan["retroactive_check"] == False:
                    problem_counter = problem_counter + 1
            return render_template("location_info.html", id = loc_id, name = location["name"], address = location["address"], scans = scan_counter, problems = problem_counter, active = "locations", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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
            user_is_scanner = user["scanner_perm"]
            user_is_admin = user["admin_perm"]
            logged_in = True
            return render_template("start_scanning.html", loc_names = loc_names, loc_ids = loc_ids, r = locations.find().count(), active = "scan", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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
            user_is_scanner = user["scanner_perm"]
            user_is_admin = user["admin_perm"]
            logged_in = True
            return render_template("scan_neutral.html", loc_name = loc_name, loc_id = loc_id, time = time.time(), active = "scan", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in)
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
            elif db.locations.find_one({"_id": ObjectId(loc_id)}) == None:
                print(loc_id)
                return "error"

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

@app.route("/positive")
def positive():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        else:
            return render_template("positive.html", name = user["name"])
    else:
        return redirect(url_for("serve_login"))


@app.route("/positive/confirm")
def confirm_positive():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        else:
            cali_time = time.time() - 28800
            fortnite = cali_time - 1209600
            exposurelists = db.exposurelists
            people_exposed = []
            checkins = db.checkins
            for user_check in checkins.find({"user_id": user["_id"], "time": {"$gt": fortnite}}):
                print("Checking host's checkin" + str(user_check["time"]))
                user_check["retroactive_check"] = False
                checkins.replace_one({"_id": user_check["_id"]}, user_check)
                mt = (user_check["time"] - 600)
                pt = (user_check["time"] + 600)
                #print(list(db.checkins.find({"loc_id": user_check["loc_id"], "time": {"$gt": mt}, "time": {"$lt", pt}})))
                for other_check in db.checkins.find({"loc_id": user_check["loc_id"], "time": {"$gt": mt}, "time": {"$lt": pt}}):
                    print("Checking other person's checkin at " + users.find_one({"_id": other_check["user_id"]})["name"])
                    if(other_check["user_id"] != user["_id"]):
                        update_exposure = users.find_one({"_id": other_check["user_id"]})
                        update_exposure["exposures"].append(strftime("%Y-%m-%d" , gmtime(other_check["time"])))
                        users.replace_one({"_id": other_check["user_id"]}, update_exposure)
                    add_user = True
                    for u in people_exposed:
                        if u == other_check["user_id"]:
                            add_user = False
                    if (add_user) and (other_check["user_id"] != user["_id"]):
                        people_exposed.append(other_check["user_id"])

            enable_twilio = False
            for peep in people_exposed:
                belonging_peep = users.find_one({"_id": peep})
                recent_exposure = belonging_peep["exposures"][-1]
                print("Send message to " + belonging_peep["phone_number"] + " for exposure on date " + recent_exposure)
                if(enable_twilio):
                    try:
                        message = twilio_client.messages.create(
                            body='Hello from symptom.space! This is an alert that you may have been in proximity of someone with COVID-19 as early as ' + recent_exposure + '. Please head to our website for a more detailed list of dates.',
                            from_='+16504494733',
                            to='+1' + belonging_peep["phone_number"]
                        )
                    except:
                        print("There was a problem sending a text")

            new_el = {
                "exposure_host": user["_id"],
                "reported_time": cali_time,
                "reported_day": strftime("%Y-%m-%d" , gmtime(cali_time)),
                "people_exposed": people_exposed
            }
            exposurelists.insert_one(new_el)
            print("DONEEEE!")
            return render_template("positive_confirm.html")
    else:
        return redirect(url_for("serve_login"))

@app.route("/map")
def map():
    if "session_id" in session:
        users = db.users
        session_id = session['session_id']
        user = users.find_one({"session_id": session_id})
        if user == None:
            return redirect(url_for("logout"))
        elif user["admin_perm"] != True:
            return "Unauthorized"
        else:
            lats = []
            longs = []
            scans = []
            problems = []
            id = []
            locations = db.locations
            for loc in locations.find():
                geocode_result = gmaps.geocode(loc["address"])
                print(geocode_result[0]["geometry"]["location"])
                lats.append(geocode_result[0]["geometry"]["location"]["lat"])
                longs.append(geocode_result[0]["geometry"]["location"]["lng"])
                problem_counter = 0
                scan_counter = 0
                cali_time = time.time() - 28800
                fortnite = cali_time - 1209600
                for scan in db.checkins.find({"loc_id": loc["_id"], "time": {"$gt": fortnite}}):
                    scan_counter = scan_counter + 1
                    if scan["retroactive_check"] == False:
                        problem_counter = problem_counter + 1
                problems.append(problem_counter)
                scans.append(scan_counter)
                id.append(str(loc["_id"]))
            user_is_scanner = user["scanner_perm"]
            user_is_admin = user["admin_perm"]
            logged_in = True
            print(id)
            return render_template("map.html", active = "map", is_scanner = user_is_scanner, is_admin = user_is_admin, logged_in = logged_in, r = len(id), lats = lats, longs = longs, scans = scans, problems = problems, id = id)
    else:
        return redirect(url_for("serve_login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    f = open("./secrets/secret_key.txt", "r")
    app.secret_key = f.read(25)
    app.run()
