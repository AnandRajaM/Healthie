from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
import os

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
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return f'Welcome {username}'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
