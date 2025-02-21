import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import sys
import requests
import re
import urllib.parse
from datetime import datetime
import requests
from musicLibrary import music

sys.path.append(os.path.expanduser("~") + "\\AppData\\Roaming\\Python\\Python311\\site-packages")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower().strip()
            print(f"DEBUG: Raw recognized command: '{command}'")  # Print exact text
            return command
        except sr.UnknownValueError:
            print("Couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Recognition service error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        return ""

def search_duckduckgo(query):
    search_url = f"https://www.duckduckgo.com/?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    speak(f"Searching DuckDuckGo for {query}.")

def tell_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")
    speak(f"The time is {current_time}")

def tell_joke():
    joke_url = "https://v2.jokeapi.dev/joke/Any?format=txt"
    try:
        response = requests.get(joke_url)
        joke_data = response.text
        speak(joke_data if joke_data else "Sorry, I couldn't find a joke right now.")
    except Exception as e:
        speak("Sorry, I couldn't fetch a joke.")
        print(f"Joke API Error: {e}")

def open_website(command):
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

# def play_music(command):
#     print(f"DEBUG: Entering play_music with command: {command}")
#     query = command.replace("play", "").strip()
#     if "by" in query:
#         song, artist = query.split("by", 1)
#         song, artist = song.strip(), artist.strip()
#         search_query = f"{song} {artist} song"
#     else:
#         search_query = f"{query} song"
#     youtube_search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
#     youtube_watch_url = f"https://www.youtube.com/embed?listType=search&list={urllib.parse.quote(search_query)}"
#     print(f"DEBUG: Opening YouTube autoplay: {youtube_watch_url}")
#     webbrowser.open(youtube_watch_url)
#     speak(f"Playing {query} on YouTube.")
def play_music(command):
    print(f"DEBUG: Entering play_music with command: {command}")
    query = command.replace("play", "").strip()
    
    if "by" in query:
        song, artist = query.split("by", 1)
        song, artist = song.strip(), artist.strip()
        search_query = f"{song} {artist} song"
    else:
        search_query = f"{query} song"

    youtube_search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
    
    # Get the first video result
    print(f"DEBUG: Fetching YouTube search results: {youtube_search_url}")
    
    response = requests.get(youtube_search_url)
    video_ids = re.findall(r"watch\?v=(\S{11})", response.text)

    if video_ids:
        first_video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        print(f"DEBUG: Opening first video: {first_video_url}")
        webbrowser.open(first_video_url)
        speak(f"Playing {query} on YouTube.")
    else:
        print("DEBUG: No video found.")
        speak("Sorry, I couldn't find that song.")


def process_command(command):
    command = command.strip()
    print(f"DEBUG: Processing command: '{command}'")  # Confirm command received
    if 'search' in command:
        query = command.replace("search", "").strip()
        print(f"DEBUG: Searching for: {query}")
        search_duckduckgo(query)
    elif 'play' in command:
        print(f"DEBUG: Detected play command: {command}")
        play_music(command)
    elif 'time' in command or 'what is the time' in command or "what's the time" in command:
        print(f"DEBUG: Telling time")
        tell_time()
    elif 'joke' in command:
        print(f"DEBUG: Fetching a joke")
        tell_joke()
    elif 'open' in command:
        print(f"DEBUG: Opening website")
        open_website(command)
    else:
        print(f"DEBUG: Unrecognized command: {command}")
        speak("I didn't catch that. Can you repeat?")

def main():
    speak("Say 'Jarvis' to wake me up...")
    while True:
        command = listen_for_command()
        if 'jarvis' in command:
            speak("Listening for your command...")
            process_command(command.replace("jarvis", "").strip())  # Process command immediately

if __name__ == "__main__":
    main()

# import pyttsx3
# import speech_recognition as sr
# import webbrowser
# import os
# import sys
# from datetime import datetime
# import requests
# from musicLibrary import music

# # Ensure correct Python version path if needed
# sys.path.append(os.path.expanduser("~") + "\\AppData\\Roaming\\Python\\Python311\\site-packages")

# # Initialize text-to-speech engine
# def speak(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

# # Listen for a command with optimized recognition
# def listen_for_command():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening for command...")
#         recognizer.adjust_for_ambient_noise(source, duration=1)
#         try:
#             audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
#             command = recognizer.recognize_google(audio).lower()
#             print(f"DEBUG: Heard command: {command}")
#             return command
#         except sr.UnknownValueError:
#             print("Couldn't understand the audio.")
#         except sr.RequestError as e:
#             print(f"Recognition service error: {e}")
#         except Exception as e:
#             print(f"Error: {e}")
#         return ""

# # Search function using DuckDuckGo
# def search_duckduckgo(query):
#     search_url = f"https://www.duckduckgo.com/?q={query.replace(' ', '+')}"
#     webbrowser.open(search_url)
#     speak(f"Searching DuckDuckGo for {query}.")

# # Tell current time
# def tell_time():
#     current_time = datetime.now().strftime("%H:%M:%S")
#     print(f"Current time: {current_time}")
#     speak(f"The time is {current_time}")

# # Fetch and tell a joke
# def tell_joke():
#     joke_url = "https://v2.jokeapi.dev/joke/Any?format=txt"
#     try:
#         response = requests.get(joke_url)
#         joke_data = response.text
#         speak(joke_data if joke_data else "Sorry, I couldn't find a joke right now.")
#     except Exception as e:
#         speak("Sorry, I couldn't fetch a joke.")
#         print(f"Joke API Error: {e}")

# # Open a website based on command
# def open_website(command):
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

# # Play music from YouTube Music or search on streaming platforms
# # def play_music(command):
# #     query = command.replace("play", "").strip()
# #     if query in music:
# #         webbrowser.open(music[query])
# #         speak(f"Playing {query} from your library.")
# #     else:
# #         search_query = f"{query} song on YouTube"
# #         search_duckduckgo(search_query)
# #         speak(f"Searching for {query} on YouTube.")
# def play_music(command):
#     """Plays music from YouTube or searches on Spotify."""
#     print(f"DEBUG: Entering play_music with command: {command}")  # Debug print

#     query = command.replace("play", "").strip()

#     if "by" in query:
#         song, artist = query.split("by", 1)
#         song, artist = song.strip(), artist.strip()
#         search_query = f"{song} {artist} song"
#     else:
#         search_query = f"{query} song"

#     print(f"DEBUG: Searching YouTube for: {search_query}")  # Confirm search phrase

#     # Open YouTube search results
#     youtube_search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
#     webbrowser.open(youtube_search_url)
#     speak(f"Searching YouTube for {search_query}.")


# Process user command
# def process_command(command):
#     print(f"DEBUG: Processing command: {command}")
#     if 'search' in command:
#         query = command.replace("search", "").strip()
#         search_duckduckgo(query)
#     elif 'play' in command:
#         play_music(command)
#     elif 'time' in command:
#         tell_time()
#     elif 'joke' in command:
#         tell_joke()
#     elif 'open' in command:
#         open_website(command)
#     else:
#         speak("I didn't catch that. Can you repeat?")
def process_command(command):
    print(f"DEBUG: Processing command: {command}")  # Confirm command received
    if 'search' in command:
        query = command.replace("search", "").strip()
        search_duckduckgo(query)
    elif 'play' in command:
        print(f"DEBUG: Detected play command: {command}")  # Add debug here
        play_music(command)
    elif 'time' in command:
        tell_time()
    elif 'joke' in command:
        tell_joke()
    elif 'open' in command:
        open_website(command)
    else:
        speak("I didn't catch that. Can you repeat?")

# Main function to run the assistant
def main():
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
#             audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
#             command = recognizer.recognize_google(audio).lower()
#             print(f"DEBUG: Heard command: {command}")
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
#     """Tells the current time and prints it."""
#     current_time = datetime.now().strftime("%H:%M:%S")
#     print(f"The current time is {current_time}")
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
#     print(f"DEBUG: Processing command: {command}")
#     if 'search' in command:
#         query = command.replace("search", "").strip()
#         search_duckduckgo(query)
#     elif 'play' in command:
#         query = command.replace("play", "").strip()
#         search_duckduckgo(f"{query} song")
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

