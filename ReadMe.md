Jarvis - Voice Assistant

Jarvis is a voice-controlled assistant built using Python. It can recognize voice commands, search the web, tell jokes, announce the time, and open websites.

Features

Voice Recognition: Listens and processes voice commands.

Text-to-Speech: Responds using speech synthesis.

Web Search: Searches queries on DuckDuckGo.

Time Announcement: Tells the current time.

Joke Telling: Fetches and tells a random joke.

Website Opening: Opens popular websites like Google, YouTube, and Facebook.

Installation

Prerequisites

Ensure you have Python 3.11+ installed.

Install the required dependencies:

pip install pyttsx3 speechrecognition requests

Usage

Run the assistant using:

python main.py

Say "Jarvis" to activate it, then give a command such as:

"Search Python programming"

"What is the time?"

"Tell me a joke"

"Open YouTube"

Environment Variables

If using an API key, store it in an .env file and load it with:

from dotenv import load_dotenv
load_dotenv()

Contributing

Feel free to fork this project and submit pull requests!

License

This project is open-source under the MIT License.