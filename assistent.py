import os
import webbrowser
import requests
import json
import speech_recognition as sr
import pyttsx3
# from keys import openai_api_key
from openai import OpenAI

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's voice command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language="en-US")
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return ""

# Function to get user input (voice or text)
def get_user_input():
    print("Would you like to use voice or text commands? (voice/text)")
    mode = input().strip().lower()
    if mode == "voice":
        return listen()
    elif mode == "text":
        return input("Type your command: ").strip().lower()
    else:
        speak("Invalid mode. Please choose voice or text.")
        return ""

# Function to open YouTube
def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

# Function to get news updates
def get_news():
    api_key = "21b88ad45c40407ebf76abedd25846b4"  # Replace with your News API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    news_data = json.loads(response.text)

    speak("Here are the top news headlines")
    for i, article in enumerate(news_data["articles"][:5]):
        speak(f"News {i+1}: {article['title']}")
        print(article["title"])

# Function to perform system updates (simulated)
def system_update():
    speak("Checking for system updates")
    # Simulate a system update check
    speak("Your system is up to date") 

def openAI():
    client = OpenAI(api_key='write api key ')
#prompt
    user_input =input("enter text :")

    response = client.images.generate(model="dall-e-3" , prompt=user_input , size='1024x1024', quality='hd',n=1,style='vivid')
    image_url = response.data[0].url
    print(image_url)

# Function to handle the virtual assistant's main loop
def virtual_assistant():
    speak("Hello, I am your virtual assistant. How can I help you today?")
    while True:
        command = get_user_input()

        if "open youtube" in command:
            open_youtube()
        elif "news" in command:
            get_news()
        elif "system update" in command:
            system_update()
        elif "generate image" in command:
            openAI()
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            speak("I am not sure how to help with that. Please try again.")

# Run the virtual assistant
if __name__ == "__main__":
    virtual_assistant()