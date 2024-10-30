"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

import speech_recognition as sr
recognizer=sr.Recognizer()

def capture_voice_input():
    global audio

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def convert_voice_to_text():
    global audio
    global text
    try:
        text = recognizer.recognize_google(audio)
        print("You: ",text)
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))



# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="You are an expert at creating professional summary for resume of a fresher. Include short, formal sentences to make it look professional"
  )

history=[]
print("Bot: Hello how may I help you today?")
print()

def chat():
  global text
  global audio

  print("Voice input or text?")
  print("Enter 1 for voice input and 2 for text input")
  choice=int(input("Enter your choice: "))
  if choice==2: 
    while True:
        user_input=input("You: ")
        print()
        chat_session = model.start_chat(
        history=history
        )

        response = chat_session.send_message(user_input)
        model_response=response.text

        print("Bot: ",model_response)
        print()

        history.append({"role":"user","parts":[user_input]})
        history.append({"role":"model","parts":[model_response]})
  else: 
    
    while True:
        capture_voice_input()
        convert_voice_to_text()
        user_input=text
        print()
        chat_session = model.start_chat(
        history=history
        )

        response = chat_session.send_message(user_input)
        model_response=response.text

        print("Bot: ",model_response)
        print()

        history.append({"role":"user","parts":[user_input]})
        history.append({"role":"model","parts":[model_response]})  
chat()