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
# Sample to check how data is store in firestore (dictionarie of values)
# ----------------------------------------
docs = db.collection("users").stream()
for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")    #doc id is a unique identifier for each document/user in the collection


# ----------------------------------------
# Sample to get username and pass of all users in db
# ----------------------------------------




for doc in docs:
    firebase_timestamp = (doc.to_dict()['appointments'][1])
    if datetime.datetime.now(tz=pytz.UTC) >= firebase_timestamp:
        print("ok")
    else:
        print("Reminder is not due yet.")