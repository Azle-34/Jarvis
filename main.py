import speech_recognition as sr
import pyttsx3
import webbrowser

recognizer = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

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

    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "exit" in c.lower() or "shutdown" in c.lower():
        speak("Goodbye!")
        exit()

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r=sr.Recognizer()
        print("Say 'Jarvis' to activate the assistant.")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            print("You said: " + word)
            if "jarvis" in word.lower():
                speak("Jarvis Active")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    speak("hello sir, what can I do for you?")
                    audio = r.listen(source)

                    command = r.recognize_google(audio)
                    print("You said: " + command)
                    processCommand(command)
            elif "exit" in word.lower() or "shutdown" in word.lower():
                speak("Goodbye!")
                exit()

        except sr.UnknownValueError:
            print("Didn't catch that, listening again...")
        except sr.RequestError as e:
            print("Speech service error: {0}".format(e))
        except Exception as e:
            print("Error: {0}".format(e))