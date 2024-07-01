![App Screenshot](https://raw.githubusercontent.com/AnandRajaM/Healthie/main/readme%20imgs/logo.png)


## Overview
Healthie, developed by the a² Team for the Prasunethon Hackathon, represents a cutting-edge healthcare assistant, integrating advanced technologies into a custom WhatsApp bot and a sophisticated web platform. Our solution is meticulously designed to enhance healthcare management with a suite of features including an intelligent symptom checker, timely appointment reminders, and tailored health advice. By leveraging the latest in machine learning and artificial intelligence, Healthie provides users with reliable, personalized healthcare insights and support. Our professional approach ensures a seamless, user-friendly experience, making Healthie an indispensable tool for modern healthcare management.

## Key Features
- Symptom Checker: Enables users to input symptoms and receive accurate health assessments and initial recommendations.
- Healthcare Needs Reminder: Sends automated reminders for medication schedules and upcoming doctor appointments to ensure adherence to healthcare routines.
- Access to Nearby Hospitals: Provides geolocation-based information on nearby hospitals and healthcare facilities for immediate medical assistance.
- Personalized Healthcare Advice: Delivers tailored health advice and recommendations based on user-specific health data and preferences.
- Appointment Scheduling: Facilitates seamless scheduling of medical appointments directly through the platform, enhancing user convenience.
- Healthcare Companion: Acts as a virtual healthcare companion, offering continuous support and information on health-related queries and concerns.
- Health Records Management: Utilizes Firestore from Firebase to securely store and manage user health records, ensuring accessibility and confidentiality.
- Mental Health Support: Includes resources and guidance for mental health management, promoting holistic well-being.
- PDF Generation: Generates detailed PDF reports summarizing medical queries and health records for easy sharing and archival.

## Watch our Project Video
https://github.com/AnandRajaM/Healthie/assets/142321494/a9e1937a-ddd1-41d2-8360-e6978d70703f

## Screenshots
![App Screenshot](https://raw.githubusercontent.com/AnandRajaM/Healthie/main/readme%20imgs/page.png)
![App Screenshot](https://raw.githubusercontent.com/AnandRajaM/Healthie/main/readme%20imgs/page2.png)
![App Screenshot](https://raw.githubusercontent.com/AnandRajaM/Healthie/main/readme%20imgs/page3.png)
![App Screenshot](https://raw.githubusercontent.com/AnandRajaM/Healthie/main/readme%20imgs/img.png)
![App Screenshot](https://raw.githubusercontent.com/AnandRajaM/Healthie/main/readme%20imgs/img1.png)
## Technologies Used
### Frontend
- HTML
- CSS
- Tailwind CSS
- JavaScript
- Flask 

### Backend
- Firebase Firestore

### Whatsapp Bot
- PyWa (Wrapper)
- Whatsapp API
- Flask
- SerpAPI
- Gemini 
- PyPDF & reportlabs

### ML Model


## Environment Variables 

To run this project, you will need to add the following environment variables to your .env file

For Whatsapp Bot : `ACCESS_TOKEN`
`APP_ID`
`APP_SECRET`




If your using a test number : `RECIPIENT_WAID` `PHONE_NUMBER_ID`

You can find all the env variables [here](https://developers.facebook.com/).


## API's Used

Before running the Healthie project, ensure you integrate the following API keys for seamless functionality:

#### Firebase Firestore :
Get the firestore .json file to establish a connection to the databse, you can get the file [here](https://firebase.google.com/docs/firestore). Add the path to the file in the firebase_service file.

#### SerpAPI :
To enable google searches , you must add the SerpAPI key to serpapi_service file. Obtain the key [here](https://serpapi.com/).

#### Gemini (Optional)
You can either use the gemini api or a custom model to avail AI features , if you wish to use the API , you can find it [here](https://ai.google.dev/).
## Deployment

To deploy Healthie, follow these steps:

#### 1. Clone the Repo
```bash
  git clone https://github.com/AnandRajaM/Healthie.git
  cd healthie-project
```
### 2. Install Dependencies:
```bash
  pip install -r requirements.txt
```

### 3. Configure the .env file
### 4. Add the API Keys 

### 4. Run the Website flask app
```bash
  python app.py
```

### 5. Enable port forwarding on the port 8000 (Or configure as per your needs) (Ensure port is set to PUBLIC)

### 6. Add the callback url and verify token

### 7. Run the Bot Flask app
```bash
  python main.py
```





## Authors

- Anand Raja Mohan [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anandrajam/) [![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AnandRajaM)

- Atharv Rastogi [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/atharv-rastogi-b9612a278/) [![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Atharv714)


- Aabir [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com) [![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/aabir-2004)
