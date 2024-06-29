from pywa import WhatsApp,types,filters
from pywa.types import CallbackData, User
from dataclasses import dataclass
from dotenv import load_dotenv
import os
from flask import Flask
import logging
from pywa.types import Message, CallbackButton, Button

# --------------------------------------------------------------
# Initialize the Flask app
# --------------------------------------------------------------
flask_app = Flask(__name__)
flask_app.config["DEBUG"] = True
# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


# --------------------------------------------------------------
# Initialize the WhatsApp object
# --------------------------------------------------------------

wa = WhatsApp(
    phone_id=f"{PHONE_NUMBER_ID}",
    token=f"{ACCESS_TOKEN}",
    server=flask_app,
    callback_url='',
    verify_token="",
    app_id=APP_ID,
    app_secret=f"{APP_SECRET}",
)
print("Success")


# --------------------------------------------------------------
# Define the data class to store user data and message
# --------------------------------------------------------------

@dataclass(frozen=True, slots=True) # Do not use kw_only=True
class UserData(CallbackData): # Subclass CallbackData
    id: int
    name: str | None
    message : str | None = None

# --------------------------------------------------------------
# Define the message handler
# --------------------------------------------------------------

@wa.on_message()
def message_handler(_: WhatsApp, msg: Message):
    if (msg.text).lower() == "hi" or msg.text == "hello":
        print("got it")
        wa.send_image(
            to=msg.from_user.wa_id,
            image = "https://cdn-icons-png.freepik.com/256/9437/9437514.png?semt=ais_hybrid",
            caption ="Hello! How can I help you today?",
            footer = "This is a footer",
            buttons=[
            Button(
                title='YO click here',
                callback_data=UserData(id=1, name='testbtn', message = "Hello this is cool"),
        ),
        
    ]

        )
@wa.on_callback_button(factory=UserData) # Use the factory parameter to convert the callback data
def on_user_data(client: WhatsApp, btn: CallbackButton[UserData]): # For autocomplete
    wa.send_message(
        to=btn.from_user.wa_id,
        text=btn.data.message,
    )



flask_app.run(port=8000)