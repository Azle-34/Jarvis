import speech_recognition as sr
import pyttsx3
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    pass

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r=sr.Recognizer()
        print("Say 'Jarvis' to activate the assistant.")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=10)
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("Yes, I am listening.")
                with sr.Microphone() as source:
                    print("Yes Sir, How may i help you?")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
        except Exception as e:
            print("Error: {0}".format(e))
            break