import speech_recognition as sr
import edge_tts
import asyncio
import webbrowser
import requests
import os
import re
import pygame
import time
import random
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("NEWS_API_KEY")
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.2

pygame.mixer.init()

def speak(text):
    async def generate_and_play():
        try:
            communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural")
            await communicate.save("response.mp3")
            pygame.mixer.music.load("response.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()  
            os.remove("response.mp3")
        except Exception as e:
            print(f"[TTS error] Could not speak: {e}")
            
    asyncio.run(generate_and_play())

def try_fast_path(c):
    """
    Returns True if a fast, keyword-matched command was handled.
    Returns False if nothing matched — signals we should fall through to Gemini.
    """
    command = c.lower().strip()

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return True

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        return True

    if "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
        return True

    if "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
        return True

    if "open notepad" in command:
        speak("Opening Notepad")
        os.startfile("notepad.exe")
        return True

    if "open calculator" in command:
        speak("Opening Calculator")
        os.startfile("calc.exe")
        return True

    if "open command" in command:
        speak("Opening Command Prompt")
        os.startfile("cmd.exe")
        return True

    if "open camera" in command:
        speak("Opening Camera")
        os.startfile("microsoft.windows.camera:")
        return True

    if "exit" in command or "shutdown" in command:
        speak("Jarvis exiting!")
        exit()

    if re.search(r'\d+\s*[\+\-\*/]\s*\d+', command):
        try:
            expr = re.search(r'[\d\.\+\-\*/\s\(\)]+', command).group()
            result = eval(expr)
            speak(f"The answer is {result}")
            return True
        except Exception:
            pass

    if len(command.split()) <= 2:
        speak("Can you say that again with a bit more detail?")
        return True

    return False

tools = [
    types.Tool(function_declarations=[
        types.FunctionDeclaration(
            name="play_song",
            description="Plays a song, artist, or music genre on YouTube",
            parameters=types.Schema(
                type="OBJECT",
                properties={"song_name": types.Schema(type="STRING")},
                required=["song_name"]
            )
        ),
        types.FunctionDeclaration(
            name="calculate",
            description="Performs a math calculation",
            parameters=types.Schema(
                type="OBJECT",
                properties={"expression": types.Schema(type="STRING", description="e.g. '5 + 3', '20 percent of 80'")},
                required=["expression"]
            )
        ),
        types.FunctionDeclaration(
            name="get_news",
            description="Fetches and reads the latest news headlines",
            parameters=types.Schema(type="OBJECT", properties={})
        ),
    ])
]

GEMINI_CONFIG = types.GenerateContentConfig(
    tools=tools,
    system_instruction="""You are Jarvis, a calm and efficient voice assistant.
RULES:
1. If the user's request clearly matches one of your available functions, call it directly. Do not explain what you're about to do — just call the function.
2. If a request is close to a function but missing required info you cannot reasonably infer (e.g. "play a song" with no song name), respond with ONE short spoken question to get that missing detail. Do not call the function yet.
3. If a request has no matching function at all, say so briefly and naturally, e.g. "I can't do that yet, sir." Do not pretend to call a function that doesn't exist.
4. If a request is vague but a reasonable default exists (e.g. "play some music" → pick a popular, safe default song), make a sensible choice and call the function rather than asking.
5. Keep all spoken responses short — one sentence, no more than 15 words. This will be converted to speech, so avoid long explanations, lists, or markdown formatting.
6. Never break character or mention that you are an AI model, Gemini, or a language model. You are Jarvis.
""",
    max_output_tokens=200,
)


def ask_gemini(command, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=command,
                config=GEMINI_CONFIG,
            )
            return response.candidates[0].content.parts[0]

        except Exception as e:
            error_str = str(e)
            is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str

            if is_rate_limit and attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"[Rate limited] Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                print(f"[Gemini error] {e}")
                return None

    return None

def handle_gemini_response(part):
    if part.function_call:
        name = part.function_call.name
        args = dict(part.function_call.args)

        if name == "play_song":
            play_song(args.get("song_name"))

        elif name == "calculate":
            try:
                expr = args.get("expression").replace("percent of", "/100*")
                result = eval(expr)
                speak(f"The answer is {result}")
            except Exception:
                speak("Sorry, I couldn't calculate that")

        elif name == "get_news":
            fetch_news()

    else:
        speak(part.text)

def play_song(song_name):
    import pywhatkit
    speak(f"Playing {song_name}")
    pywhatkit.playonyt(song_name)


def fetch_news():
    try:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}",
            timeout=5
        )
        if r.status_code == 200:
            articles = r.json().get("articles", [])[:3]
            if not articles:
                speak("No news articles found right now")
                return
            speak("Here are the top headlines")
            for article in articles:
                speak(article["title"])
        else:
            speak("Sorry, I couldn't fetch the news right now")
    except requests.exceptions.RequestException:
        speak("I couldn't connect to the news service")


def processCommand(c):
    if try_fast_path(c):
        return
    part = ask_gemini(c)
    if part is None:
        speak("Sorry, I'm having trouble reaching my brain right now.")
        return
    handle_gemini_response(part)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        print("Say 'Jarvis' to activate the assistant.")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = recognizer.listen(source, phrase_time_limit=8)
            word = recognizer.recognize_google(audio)
            print("You said: " + word)

            if "jarvis" in word.lower():
                speak("hello sir, what can I do for you?")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, phrase_time_limit=8)
                command = recognizer.recognize_google(audio)
                print("You said: " + command)
                processCommand(command)

            elif "exit" in word.lower() or "shutdown" in word.lower():
                speak("Jarvis Exiting!")
                exit()

        except sr.UnknownValueError:
            print("Didn't catch that, listening again...")
        except sr.RequestError as e:
            print("Speech service error:", e)
        except Exception as e:
            print("Error:", e)