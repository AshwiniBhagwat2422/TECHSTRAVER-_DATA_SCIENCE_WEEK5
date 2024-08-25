import speech_recognition as sr
import pyttsx3
import time
import sys

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  
engine.setProperty('volume', 0.9)  

def process_command(command):
    command = command.lower()
    print(f"Processing command: {command}")  
    if "time" in command:
        return time.strftime("%I:%M %p")
    elif "date" in command:
        return time.strftime("%Y-%m-%d")
    elif "joke" in command:
        return "Why don't skeletons fight each other? Because they don't have the guts!"
    elif "capital of" in command:
        if "france" in command:
            return "The capital of France is Paris."
        elif "india" in command:
            return "The capital of India is Delhi."
        elif "italy" in command:
            return "The capital of Italy is Rome."
    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        sys.exit()    
    else:
        return "Sorry, I didn't understand that command."

def speak(text):
    engine.say(text)
    engine.runAndWait()


with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)  
    print("Listening for the wake word...")
    while True:
        try:
            audio = recognizer.listen(source, timeout=10)  
            print("Audio captured")
            command = recognizer.recognize_google(audio)
            command = command.lower()  
            print(f"Recognized command: {command}")
            if "hey assistant" in command:
                response = process_command(command)
                print(f"Response: {response}")
                speak(response)
            else:
                print("No wake word detected.")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.WaitTimeoutError:
            print("Listening timed out; please try again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        time.sleep(1)