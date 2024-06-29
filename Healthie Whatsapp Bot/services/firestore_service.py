import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import pytz

# ----------------------------------------
# Initialize Firestore DB
# ----------------------------------------
cred = credentials.Certificate(r"D:\dev\healthie-648dd-firebase-adminsdk-vewrw-276a6a08fb.json")   #i sent the admin fle in zip
firebase_admin.initialize_app(cred)

# ----------------------------------------
# Initialize Firestore DB
# ----------------------------------------
db = firestore.client()

# ----------------------------------------
# Adding a new Reminder for user to db (using phone number)
# ----------------------------------------
def add_reminder(phone_number,medication_name, reminder_time):
    try:
        c=0
        docs = db.collection("users").stream()
        for doc in docs:
            try:
                if doc.to_dict()['number'] == phone_number:
                        c+=1
                        #adding the new reminder to user's reminders
                        db.collection("users").document(doc.id).update({
                            "reminders": firestore.ArrayUnion([{
                                "medication": medication_name,
                                "time": reminder_time
                            }])
                        })
                        return True
            except:
                pass

        if c==0:
            #add new user and set reminder
            db.collection("users").add({
                "number": phone_number,
                "reminders": [{
                    "medication": medication_name,
                    "time": reminder_time
                }]
            })
            return True
        
    except Exception as e:
        print(e)
        return False

# ----------------------------------------
# Returing all reminders for a user
# ----------------------------------------
def get_reminders(phone_number):
    c=0
   
    docs = db.collection("users").stream()
    for doc in docs:
        try:
            if doc.to_dict()['number'] == phone_number:
                c+=1
                return doc.to_dict()['reminders']     
        except:
            pass

    if c==0:
        return []
        
    
# ----------------------------------------
# Adding a new Appointment for user to db (using phone number)
# ----------------------------------------
def add_appointment(phone_number,doctor_name, appointment_time):
    try:
        c=0
        docs = db.collection("users").stream()
        for doc in docs:
            try:
                if doc.to_dict()['number'] == phone_number:
                        c+=1
                        #adding the new reminder to user's reminders
                        db.collection("users").document(doc.id).update({
                            "appointments": firestore.ArrayUnion([{
                                "doctor": doctor_name,
                                "time": appointment_time
                            }])
                        })
                        return True
            except:
                pass

        if c==0:
            #add new user and set reminder
            db.collection("users").add({
                "number": phone_number,
                "appointments": [{
                    "doctor": doctor_name,
                    "time": appointment_time
                }]
            })
            return True
        
    except Exception as e:
        print(e)
        return False

# ----------------------------------------
# Returing all appointments for a user
# ----------------------------------------
def get_appointments(phone_number):
    c=0
   
    docs = db.collection("users").stream()
    for doc in docs:
        try:
            if doc.to_dict()['number'] == phone_number:
                c+=1
                return doc.to_dict()['appointments']     
        except:
            pass

    if c==0:
        return []
    

        