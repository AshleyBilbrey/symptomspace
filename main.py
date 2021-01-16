from flask import Flask, request, render_template
from pymongo import MongoClient
import re
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
        phonenumber = request.form["phone-number"]
        search = re.search("[0-9]{10}", phonenumber)
        if search = None:
            return "That's not a valid phone number!"
        else:
            return "You tried to log in with phone number #" + phonenumber
    else:
        return "Error"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
   app.run()
