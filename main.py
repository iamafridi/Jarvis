import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import sys
from datetime import datetime
import requests

# Ensure correct Python version path if needed
sys.path.append(os.path.expanduser("~") + "\\AppData\\Roaming\\Python\\Python311\\site-packages")

def speak(text):
    """Makes the assistant speak out."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Listens for audio command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
            command = recognizer.recognize_google(audio).lower()
            print(f"DEBUG: Heard command: {command}")
            return command
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
        except Exception as e:
            print(f"Speech recognition error: {e}")
        return ""

def search_duckduckgo(query):
    """Searches for a query on DuckDuckGo and opens the first result."""
    search_url = f"https://www.duckduckgo.com/?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    speak(f"Searching DuckDuckGo for {query}.")

def tell_time():
    """Tells the current time and prints it."""
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"The current time is {current_time}")
    speak(f"The current time is {current_time}")

def tell_joke():
    """Fetches and tells a random joke."""
    joke_url = "https://v2.jokeapi.dev/joke/Any?format=txt"
    try:
        response = requests.get(joke_url)
        joke_data = response.text
        speak(joke_data if joke_data else "Sorry, I couldn't find a joke right now.")
    except Exception as e:
        speak("Sorry, I couldn't fetch a joke at the moment.")
        print(f"Joke API Error: {e}")

def open_website(command):
    """Opens a website based on command."""
    websites = {
        "facebook": "https://www.facebook.com",
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "twitter": "https://www.twitter.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
    }
    for site in websites:
        if site in command:
            webbrowser.open(websites[site])
            return
    if "open" in command:
        site = command.replace("open", "").strip()
        webbrowser.open(f"https://{site}.com")
    else:
        speak("I didn't understand which site to open.")

def process_command(command):
    """Processes the given command."""
    print(f"DEBUG: Processing command: {command}")
    if 'search' in command:
        query = command.replace("search", "").strip()
        search_duckduckgo(query)
    elif 'play' in command:
        query = command.replace("play", "").strip()
        search_duckduckgo(f"{query} song")
    elif 'time' in command:
        tell_time()
    elif 'joke' in command:
        tell_joke()
    elif 'open' in command:
        open_website(command)
    else:
        speak("I didn't catch that. Can you repeat?")

def main():
    """Main function to run the assistant loop."""
    speak("Say 'Jarvis' to wake me up...")
    while True:
        command = listen_for_command()
        if 'jarvis' in command:
            speak("Listening for your command...")
            command = listen_for_command()
            process_command(command)

if __name__ == "__main__":
    main()


# import pyttsx3
# import speech_recognition as sr
# import webbrowser
# import os
# import sys
# from datetime import datetime
# import requests

# # Ensure correct Python version path if needed
# sys.path.append(os.path.expanduser("~") + "\\AppData\\Roaming\\Python\\Python311\\site-packages")

# def speak(text):
#     """Makes the assistant speak out."""
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

# def listen_for_command():
#     """Listens for audio command."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening for command...")
#         recognizer.adjust_for_ambient_noise(source)
#         try:
#             audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
#             command = recognizer.recognize_google(audio).lower()
#             print(f"Heard: {command}")
#             return command
#         except sr.UnknownValueError:
#             print("Google Speech Recognition could not understand the audio.")
#         except sr.RequestError as e:
#             print(f"Could not request results from Google Speech Recognition service: {e}")
#         except Exception as e:
#             print(f"Speech recognition error: {e}")
#         return ""

# def search_duckduckgo(query):
#     """Searches for a query on DuckDuckGo and opens the first result."""
#     search_url = f"https://www.duckduckgo.com/?q={query.replace(' ', '+')}"
#     webbrowser.open(search_url)
#     speak(f"Searching DuckDuckGo for {query}.")

# def tell_time():
#     """Tells the current time."""
#     current_time = datetime.now().strftime("%H:%M:%S")
#     speak(f"The current time is {current_time}")

# def tell_joke():
#     """Fetches and tells a random joke."""
#     joke_url = "https://v2.jokeapi.dev/joke/Any?format=txt"
#     try:
#         response = requests.get(joke_url)
#         joke_data = response.text
#         speak(joke_data if joke_data else "Sorry, I couldn't find a joke right now.")
#     except Exception as e:
#         speak("Sorry, I couldn't fetch a joke at the moment.")
#         print(f"Joke API Error: {e}")

# def open_website(command):
#     """Opens a website based on command."""
#     websites = {
#         "facebook": "https://www.facebook.com",
#         "youtube": "https://www.youtube.com",
#         "google": "https://www.google.com",
#         "twitter": "https://www.twitter.com",
#         "instagram": "https://www.instagram.com",
#         "linkedin": "https://www.linkedin.com",
#     }
#     for site in websites:
#         if site in command:
#             webbrowser.open(websites[site])
#             return
#     if "open" in command:
#         site = command.replace("open", "").strip()
#         webbrowser.open(f"https://{site}.com")
#     else:
#         speak("I didn't understand which site to open.")

# def process_command(command):
#     """Processes the given command."""
#     if 'search' in command:
#         query = command.replace("search", "").strip()
#         search_duckduckgo(query)
#     elif 'time' in command:
#         tell_time()
#     elif 'joke' in command:
#         tell_joke()
#     elif 'open' in command:
#         open_website(command)
#     else:
#         speak("I didn't catch that. Can you repeat?")

# def main():
#     """Main function to run the assistant loop."""
#     speak("Say 'Jarvis' to wake me up...")
#     while True:
#         command = listen_for_command()
#         if 'jarvis' in command:
#             speak("Listening for your command...")
#             command = listen_for_command()
#             process_command(command)

# if __name__ == "__main__":
#     main()

