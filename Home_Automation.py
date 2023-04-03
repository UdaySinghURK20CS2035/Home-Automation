import pyttsx3
import pyfirmata
import datetime
import speech_recognition as sr
import random
from pyfirmata import Arduino, util

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    d = 'sir I am always here to help you', 'tell me how can I help you sir', 'What can I do for you sir'
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon sir!")
    else:
        speak("Good Evening sir!")
    speak("Sir I am JARVIS.")
    speak(random.choice(d))


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)
        print("Say that again Please....")
        return "None"
    return query


port = 'COM3'
board = Arduino(port)

it = util.Iterator(board)
it.start()

motor1 = board.get_pin("d:9:o")

board.digital[13].mode = pyfirmata.OUTPUT
board.digital[13].write(0)

board.digital[9].mode = pyfirmata.OUTPUT
motor1.write(1)

if __name__ == '__main__':
    wishme()
    while True:
        query = takecommand().lower()

        if 'turn on' in query or 'open' in query:
            board.digital[13].write(1)
            speak("LED turned on")

        elif 'turn off' in query:
            board.digital[13].write(0)
            speak("LED turned off")



        elif 'switch on led' in query:
            board.digital[9].write(0)
            motor1.write(0)
            speak('LED turned on')

        elif 'switch off led' in query:
            board.digital[9].write(1)
            motor1.write(1)
            speak('LED turned off')


        elif 'sleep' in query:
            speak("Thankyou Sir for using me as you assistant")
            break
