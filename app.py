from unittest.util import three_way_cmp
import datetime

from certifi import where
from flask import Flask, request, jsonify, session
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from flask_cors import CORS



dateDict = {
    "Monday":0,
    "Tuesday":1,
    "Wednesday":2,
    "Thursday":3,
    "Friday":4,
    "Saturday":5,
    "Sunday":6
    }

load_dotenv()
secret_key = os.environ.get("SECRET_KEY")
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
app.secret_key = secret_key

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

@app.route('/')
def func():
    global dateDict
    dateObject = datetime.date.today()
    print(dateDict[dateObject.strftime("%A")],"THIS IS THE TIME GANG")
    res = supabase.table('users').select("*", count = "exact").execute()

    users = res.data
    count = res.count

    print(users)

    html = ""
    for user in users:
        html += f'<p>{(str) (user["id"]) + " " + user["username"] + " " + user["email"]}</p>'

    return html

@app.route("/subjects", methods=["GET"])
def getSubjects():
    subjects = supabase.table('subjects').select("*", count = "exact").execute()
    print(subjects)

    return jsonify({"subjects":subjects.data})

@app.route("/namepet", methods=["POST"])
def savePet():
    data = request.json
    user_id = 1
    # user_id = session.get("id")
    # if not user_id:
    #     return {"error": "Unauthorized"}, 401
    petName = data["petName"]

    response = supabase.table("pet_user").insert({
        "user_id" : 1,
        "pet_id" : 1,
        "name" : "Bob"
    }).execute()

    return jsonify({"status": "updated"}), 200




@app.route("/subjects", methods=["POST"])
def saveSubject():
    data = request.json
    subjectId = data.get("id")

    if not subjectId:
        return jsonify({"error": "No subject id"}), 400

    supabase.table("users").insert({
        "id": subjectId
    })

    return jsonify({"status": "updated"}), 200


@app.route('/signup', methods=["POST"])
def createUser():
    data = request.json

    username = data["username"]
    password = data["password"]
    email = data["email"]

    response = supabase.table("users").insert({
        "username" : username,
        "password" : password,
        "email" : email
    }).execute()

    if not response.data:
        return jsonify({"status" : "error"}), 400

    user_id = response.data[0]["id"]
    session["id"] = user_id

    print("Session: ", session)

    return {"status" : "ok"}

if __name__ == '__main__':
    app.run(port=5001, debug=True) 


