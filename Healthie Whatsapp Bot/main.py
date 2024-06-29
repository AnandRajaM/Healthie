from pywa import WhatsApp,types,filters
from pywa.types import CallbackData, User
from dataclasses import dataclass
from dotenv import load_dotenv
import os
from flask import Flask
import logging
from pywa.types import Message, CallbackButton, Button, ButtonUrl
from pywa.types import SectionList, Section, SectionRow, CallbackSelection


# --------------------------------------------------------------
# Import the services
# --------------------------------------------------------------
from services import gemini_service
from services import firestore_service
from services import serpapi_service


# --------------------------------------------------------------
# Initialize the Flask app and set initial bot state
# --------------------------------------------------------------
flask_app = Flask(__name__)
flask_app.config["DEBUG"] = True

global bot_status 
bot_status = "idle"
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



# --------------------------------------------------------------
# Define the data class to store user data and message
# --------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class UserData(CallbackData): # Subclass CallbackData
    id: int
    name: str | None
    message : str | None = None

# --------------------------------------------------------------
# Define the message handler
# --------------------------------------------------------------

@wa.on_message()
def message_handler(_: WhatsApp, msg: Message):
    print(msg.text)
    if msg.text == None:
        pass
    else:
        if msg.text.lower() in ["hi", "hello", "hey","go back","back","menu","home"]:
            global bot_status
            bot_status = "idle"
            wa.send_image(
                to=msg.from_user.wa_id,
                image=r"Healthie Whatsapp Bot\images\mascot.png",
                caption="Hello! 😊 Welcome to *Healthie*, your personal healthcare assistant. How can I assist you today? Whether you need medication reminders, want to schedule an appointment, or have any healthcare-related questions, I'm here to help! 🌟",
                footer="Powered by a-squared⚡",
                buttons=[
                    Button(
                        title="Appointment",
                        callback_data=UserData(id=1, name='Schedule', message="a"),
                    ),
                    Button(
                        title="Reminders",
                        callback_data=UserData(id=2, name='Reminders', message="a"),
                    ),
                    Button(
                        title="Medical Query",
                        callback_data=UserData(id=3, name='query', message="a"),
                    ),
                ]
            )
        elif bot_status == "Chat":
            response = gemini_service.generate_response(msg.text)
            wa.send_text(
                to=msg.from_user.wa_id,
                text=response
            )

        elif bot_status == "Symptom Checker":
            response = gemini_service.generate_symptom_info(msg.text)
            wa.send_text(
                to=msg.from_user.wa_id,
                text=response
            )
            wa.send_text(
                to=msg.from_user.wa_id,
                text="If you missed any symptoms or wish to know more you may type your concerns below. \n \n To return to main menu type _*menu*_ "
            )
        
        elif bot_status == "Mental Health Support":
            response = gemini_service.generate_mental_health_conversaton(msg.text)
            wa.send_text(
                to=msg.from_user.wa_id,
                text=response
            )
        
        elif bot_status == "Nearby Hospitals":
            hospital_info = serpapi_service.get_nearby(msg.text)
            if hospital_info:
                for hospital in hospital_info:
                    bot_status = "idle"
                    wa.send_image(
                        to=msg.from_user.wa_id,
                        image=hospital[2],
                        caption=f"{hospital[0]} \n Phone: {hospital[1]} \n Location: {hospital[3]}",
                        buttons=ButtonUrl(title='View in Map', url=f"https://maps.google.com/?q={hospital[3]['latitude']},{hospital[3]['longitude']}")
                    )
            else:
                wa.send_text(
                    to=msg.from_user.wa_id,
                    text="Oops! No hospitals found nearby. Please try again later."
                )
            wa.send_text(
                to=msg.from_user.wa_id,
                text="To return to main menu type _*menu*_ "
            )

        elif bot_status == "Reminders":
            global recived_time
            if not recived_time:
                global medication_name
                medication_name = msg.text
                recived_time = True
                wa.send_text(
                    to=msg.from_user.wa_id,
                    text="Please enter the time you would like to set the reminder for. For example, type '10:00 AM' or '2:00 PM'."
                )
                
            else:
                global reminder_time

                reminder_time = msg.text
                if firestore_service.add_reminder(msg.from_user.wa_id,medication_name,reminder_time):
                    bot_status = "idle"
                    wa.send_text(
                        to=msg.from_user.wa_id,
                        text=f"Reminder set for {medication_name} at {reminder_time}."
                    )
                else:
                    bot_status = "idle"
                    wa.send_text(
                        to=msg.from_user.wa_id,
                        text="Oops! Something went wrong. Please try again later."
                    )
        
        elif bot_status == "Schedule":
            global schedule_time
            if not schedule_time:
                global doctor_name
                doctor_name = msg.text
                schedule_time = True
                wa.send_text(
                    to=msg.from_user.wa_id,
                    text="Please enter the date and time you would like to schedule the appointment for. For example, type 'Monday, 10:00 AM' or 'Friday, 2:00 PM'."
                )
            
            else:
                global appointment_time
                appointment_time = msg.text
                if firestore_service.add_appointment(msg.from_user.wa_id,doctor_name,appointment_time):
                    bot_status = "idle"
                    wa.send_text(
                        to=msg.from_user.wa_id,
                        text=f"Appointment scheduled with {doctor_name} at {appointment_time}."
                    )
                else:
                    bot_status = "idle"
                    wa.send_text(
                        to=msg.from_user.wa_id,
                        text="Oops! Something went wrong. Please try again later."
                    )




# --------------------------------------------------------------
# Define the callback button handler
# --------------------------------------------------------------

@wa.on_callback_button(factory=UserData) # Use the factory parameter to convert the callback data
def on_user_data(client: WhatsApp, btn: CallbackButton[UserData]): # For autocomplete
    global bot_status
    if bot_status == "idle":
        if btn.data.id == 3:
            wa.send_message(
                to=btn.from_user.wa_id,
                header='How can I help you today?',
                text='Select an option to receive personalized help and support from Healthie.',
                footer='Powered by a-squared⚡',
                buttons=SectionList(
                    button_title='Query Options',
                    sections=[
                        Section(
                            title='Query Options',
                            rows=[
                                SectionRow(
                                    title='Chat with Healthie ❤️',
                                    callback_data= UserData(id=1, name='chat', message=""),
                                    description='Discuss health queries with our AI chatbot, Healthie.',
                                ),
                                SectionRow(
                                    title='Symptom Checker 🔎',
                                    callback_data= UserData(id=2, name='symptom_checker', message=""),
                                    description='Check symptoms for health insights with Healthie.',
                                ),
                                SectionRow(
                                    title='Mental Health Support 🤗',
                                    callback_data= UserData(id=3, name='mental_health_support', message=""),
                                    description='Get curated mental health chat support with Healthie.',
                                ),
                                SectionRow(
                                    title='Nearby Hospitals 🏥',
                                    callback_data= UserData(id=4, name='nearby_hospitals', message=""),
                                    description='Find hospitals nearby for quick medical assistance with Healthie.',
                                ),
                                SectionRow(
                                    title='PDF Generation 📄',
                                    callback_data= UserData(id=5, name='pdf_generation', message=""),
                                    description='Generate health reports in PDF with Healthie.',
                                )
                            ],
                        ),
                    ]
                )
            )
        
        if btn.data.id == 2:
            bot_status = btn.data.name
            client.send_text(
                to=btn.from_user.wa_id,
                text="Create New Reminder - Set up a new reminder for your medications or appointments. \n \n Check Existing Reminders - View and manage your current reminders.📅 \n \n To return to main menu type _*menu*_",
                buttons=[
                    Button(
                        title="New Reminder",
                        callback_data=UserData(id=4, name='Create', message=""),
                    ),
                    Button(
                        title="Existing Reminders",
                        callback_data=UserData(id=5, name='Check', message=""),
                    ),
                ]
            )
        if btn.data.id == 1:
            bot_status = btn.data.name
            client.send_text(
                to=btn.from_user.wa_id,
                text="Create New Appointment - Schedule an appointment with a doctor. \n \n Check Existing Appointments - View and manage your current appointments. 📅 \n \n To return to main menu type _*menu*_",
                buttons=[
                    Button(
                        title="New Appointment",
                        callback_data=UserData(id=6, name='Create', message=""),
                    ),
                    Button(
                        title="Check Appointments",
                        callback_data=UserData(id=7, name='Check', message=""),
                    ),
                ]
            )
        
    if bot_status == "Reminders":
        if btn.data.id == 4:
            global recived_time
            recived_time = False
            client.send_text(
                to=btn.from_user.wa_id,
                text="Please enter the name of the medication you would like to set a reminder for."
            )
        if btn.data.id == 5:
            reminders = firestore_service.get_reminders(btn.from_user.wa_id)
            rtext = ""
            for i, reminder in enumerate(reminders, start=1):
                rtext += f"{i}. {reminder['medication']} - {reminder['time']} \n"
                rtext += f" \n \n To return to main menu type _*menu*_"
            client.send_text(
                to=btn.from_user.wa_id,
                text=rtext,
            )
    
    if bot_status == "Schedule":
        if btn.data.id == 6:
            global schedule_time
            schedule_time = False
            client.send_text(
                to=btn.from_user.wa_id,
                text="Please enter the name of the doctor to schedule an appointment with."
            )
        if btn.data.id == 7:
            appointments = firestore_service.get_appointments(btn.from_user.wa_id)
            atext = ""
            for i, appointment in enumerate(appointments, start=1):
                atext += f"{i}. {appointment['doctor']} - {appointment['time']} \n"
                atext += f" \n \n To return to main menu type _*menu*_"
            client.send_text(
                to=btn.from_user.wa_id,
                text=atext,
            )
        

   
# --------------------------------------------------------------
# Define the callback selection handler
# --------------------------------------------------------------

@wa.on_callback_selection(factory=UserData)
def on_user_data(_: WhatsApp, sel: CallbackSelection[UserData]):
    if sel.data.name == 'chat':
        global bot_status
        bot_status = "Chat"
        wa.send_image(
            to=sel.from_user.wa_id,
            image=r"Healthie Whatsapp Bot\images\talking.jpg",
            caption="You are now chatting with Healthie. Feel free to ask any health-related questions or share your concerns. I'm here to help! 🩺 \n \n To return to main menu type _*menu*_"
        )
    if sel.data.name == 'symptom_checker':
        
        bot_status = "Symptom Checker"
        wa.send_image(
            to=sel.from_user.wa_id,
            image=r"Healthie Whatsapp Bot\images\checker.png",
            caption="You are now using the Healthie Symptom Checker. Please enter the symptoms you are experiencing, separated by commas. For example, type 'fever, cough, headache'. \n \n To return to main menu type _*menu*_ "
        )
        

    if sel.data.name == 'mental_health_support':
        bot_status = "Mental Health Support"
        wa.send_image(
            to=sel.from_user.wa_id,
            image=r"Healthie Whatsapp Bot\images\mental_health.png",
            caption="You are now chatting with Healthie's mental health support. Feel free to share your thoughts, feelings, or concerns. I'm here to listen and provide support. 🌟 \n \n To return to main menu type _*menu*_ "
        )
        
    
    if sel.data.name == 'nearby_hospitals':
        bot_status = "Nearby Hospitals"
        wa.send_image(
            to=sel.from_user.wa_id,
            image=r"Healthie Whatsapp Bot\images\city.jpg",
            caption="Please share your location to find nearby hospitals. Example: 'Delhi'. \n \n To return to main menu type _*menu*_ "
        )
    
    
    if sel.data.name == 'pdf_generation':
        bot_status = "idle"
        wa.send_document(
            to=sel.from_user.wa_id,
            document=r"Healthie Whatsapp Bot\pdfs\Sample_report.pdf",
            caption="Here is a sample PDF generated by Healthie. 📄"
        )
        wa.send_text(
            to=sel.from_user.wa_id,
            text="To return to main menu type _*menu*_ "
        )

flask_app.run(port=8000)
