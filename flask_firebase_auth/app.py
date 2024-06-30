from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI


client = OpenAI(api_key=os.getenv("API_KEY"))


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize Firestore DB
cred = credentials.Certificate('flask_firebase_auth/healthie-648dd-firebase-adminsdk-vewrw-276a6a08fb.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Add new user to Firestore
        data = {
            "username": username,
            "password": password,
        }
        db.collection("users").document().set(data)
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists in Firestore
        docs = db.collection("users").where("username", "==", username).stream()
        for doc in docs:
            user = doc.to_dict()
            if user['password'] == password:
                session['username'] = username
                return redirect(url_for('profile'))
        return 'Invalid username or password'
    return render_template('loginpage2.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

from flask import Flask, render_template, request
from serpapi import GoogleSearch
from geopy.geocoders import Nominatim

# Function to get nearby hospitals based on location
def get_nearby(location, api_key):
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(location)
    if loc:
        params = {
            "engine": "google_maps",
            "q": "Hospital",
            "ll": f"@{loc.latitude},{loc.longitude},15z",
            "type": "search",
            "api_key": api_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        hospital_info = []
        for result in results.get('local_results', []):
            try:
                hospital_info.append({
                    "title": result['title'],
                    "photos_link": result.get('photos_link'),
                    "phone": result.get("phone"),
                    "website": result.get('website'),
                    "address": result['address']
                })
            except KeyError:
                continue

        return hospital_info
    return None

# Flask route to handle the form and display results
@app.route("/vhelp", methods=['GET', 'POST'])
def vhelp():
    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            api_key = "YOUR_SERPAPI_KEY_HERE"  # Replace with your actual SerpApi key
            hospitals = get_nearby(location, api_key)
            if hospitals is not None:
                return render_template("vhelp.html", hospitals=hospitals, location=location)
            else:
                return render_template("vhelp.html", error="Location not found", location=location)
        else:
            return render_template("vhelp.html", error="Please provide a location", location='')

    return render_template("vhelp.html", location='', error='')


def send_message(message):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a chatbot."},
        {"role": "user", "content": message}
    ],
    max_tokens=100,
    temperature=0.7)
    return response.choices[0].message.content

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    bot_response = send_message(user_input)
    return {'response': bot_response}

if __name__ == '__main__':
    app.run(debug=True)
