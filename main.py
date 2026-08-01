import speech_recognition as sr
import pyttsx3
import webbrowser
import music
import os

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.2

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 185)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def calculate(c):
    c = c.lower().replace("what is", "").replace("what's", "").strip()
    c = (c.replace("plus", "+")
           .replace("minus", "-")
           .replace("multiply", "*")
           .replace("times", "*")
           .replace("x", "*")
           .replace("divided by", "/"))
    print("Evaluating:", c)
    try:
        result = eval(c)
        speak(f"The answer is {result}")
    except Exception as e:
        print("Calc error:", e)  
        speak("Sorry, I couldn't calculate that")

def processCommand(c):
    if "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    
    elif any(phrase in c.lower() for phrase in ["play music", "play a song", "play a song for me", "play a song on youtube", "play a song on youtube for me"]):
        speak("What song would you like to listen to?")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, phrase_time_limit=8)
        song = recognizer.recognize_google(audio).lower()
        link = music.music.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I don't have that song.")

    elif "open notepad" in c.lower():
        speak("Opening Notepad")
        os.startfile("notepad.exe")

    elif "open calculator" in c.lower():
        speak("Opening Calculator")
        os.startfile("calc.exe")

    elif "open command" in c.lower():
        speak("Opening Command Prompt")
        os.startfile("cmd.exe")
    
    elif "open camera" in c.lower():
        speak("Opening Camera")
        os.startfile("microsoft.windows.camera:")

    elif "exit" in c.lower() or "shutdown" in c.lower():
        speak("Jarvis exiting!")
        exit()

    elif any(op in c.lower() for op in ["plus", "minus", "multiply", "times", " x ", "+", "-", "divided by"]):
        calculate(c)
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r=sr.Recognizer()
        print("Say 'Jarvis' to activate the assistant.")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = r.listen(source, phrase_time_limit=8)
            word = r.recognize_google(audio)
            print("You said: " + word)
            if "jarvis" in word.lower():
                speak("Jarvis Active")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    speak("hello sir, what can I do for you?")
                    audio = r.listen(source, phrase_time_limit=8)

                    command = r.recognize_google(audio)
                    print("You said: " + command)
                    processCommand(command)
            elif "exit" in word.lower() or "shutdown" in word.lower():
                speak("Jarvis Exiting!")
                exit()

        except sr.UnknownValueError:
            print("Didn't catch that, listening again...")
        except sr.RequestError as e:
            print("Speech service error: {0}".format(e))
        except Exception as e:
            print("Error: {0}".format(e))