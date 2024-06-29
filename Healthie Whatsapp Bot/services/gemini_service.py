import google.generativeai as genai


genai.configure(api_key = "")
model = genai.GenerativeModel('gemini-pro')


# --------------------------------------------------------------
# Create a function that generates a response based on users medical questions
# --------------------------------------------------------------

conversation_history = []
def generate_response(user_message):  
    conversation_history.append(f"Patient: {user_message}")
    if len(conversation_history) > 10:  # Limit the history to the last 10 messages
        conversation_history.pop(0)  # Remove the oldest message if history exceeds limit
    

    prompt = "You are a Medical chatbot assistant and you are chatting with a patient. Here is the conversation so far:\n"
    prompt += "\n".join(conversation_history)
    prompt += "\nChatbot responds:"

    response = model.generate_content(prompt)
    chatbot_response = response.text.strip()

    conversation_history.append(f"Chatbot: {chatbot_response}")
    if len(conversation_history) > 10:  # Ensure the history doesn't exceed the limit
        conversation_history.pop(0)
    
    return chatbot_response

# --------------------------------------------------------------
# Create a function that generates a response based on users symptoms
# --------------------------------------------------------------

conversation_symptom_history = []
def generate_symptom_info(symptoms):
    conversation_symptom_history.append(symptoms)
    if len(conversation_symptom_history) > 10:
        conversation_symptom_history.pop(0)
    
    prompt = "You are a Medical chatbot assistant and you are tasked in giving guidance on potential causes and recommended next steps based on the symptoms given by the patient. And give the response in a well structured format , preferably with bullet points. Also mention that you are a chabot and can make mistakes and not to verify the response. Here is the conversation so far:\n"
    prompt += "\n".join(conversation_symptom_history)
    prompt += "\nChatbot responds:"

    response = model.generate_content(prompt)
    chatbot_response = response.text.strip()

    conversation_symptom_history.append(chatbot_response)
    if len(conversation_symptom_history) > 10:
        conversation_symptom_history.pop(0)

    return chatbot_response

# --------------------------------------------------------------
# Create a function that generates a response based on users mental health questions
# --------------------------------------------------------------

MHS_conversation_history = []
def generate_mental_health_conversaton(user_message):
    MHS_conversation_history.append(f"Patient: {user_message}")
    if len(MHS_conversation_history) > 10:
        MHS_conversation_history.pop(0)
    
    prompt = "You are a medical chatbot assistant, supporting a patient with their mental health. Show empathy, understand their insights, and provide friendly and encouraging feedback, like a supportive friend. Here is the conversation so far:\n"
    prompt += "\n".join(MHS_conversation_history)
    prompt += "\nChatbot responds:"

    response = model.generate_content(prompt)
    chatbot_response = response.text.strip()

    MHS_conversation_history.append(f"Chatbot: {chatbot_response}")
    if len(MHS_conversation_history) > 10:
        MHS_conversation_history.pop(0)
    
    return chatbot_response