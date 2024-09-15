import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import webbrowser

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function for Jarvis to speak in the specified language (Urdu or English)
def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)  # Remove the file after playing it

# Function to take voice input from the user in both English and Urdu
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            # Try recognizing speech in English first
            command = recognizer.recognize_google(audio, language='en')
            print(f"English Detected: You said: {command}")
            return command.lower(), 'en'
        except sr.UnknownValueError:
            try:
                # If English fails, try recognizing speech in Urdu
                command = recognizer.recognize_google(audio, language='ur-PK')
                print(f"Urdu Detected: آپ نے کہا: {command}")
                return command.lower(), 'ur'
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return "None", 'none'

# Function to execute basic commands in both English and Urdu
def execute_command(command, lang):
    if "open browser" in command or "براوزر کھولو" in command:
        speak("Opening browser" if lang == 'en' else "براوزر کھول رہا ہوں", lang)
        webbrowser.open('https://www.google.com')
    elif "play music" in command or "موسیقی چلاؤ" in command:
        speak("Playing music" if lang == 'en' else "موسیقی چلا رہا ہوں", lang)
        os.system("vlc")  # VLC as an example
    elif "what is your name" in command or "تمہارا نام کیا ہے" in command:
        speak("My name is Jarvis, your personal assistant." if lang == 'en' else "میرا نام جارویس ہے، میں آپ کا ذاتی معاون ہوں۔", lang)
    elif "shutdown" in command or "سسٹم بند کرو" in command:
        speak("Shutting down the system" if lang == 'en' else "سسٹم بند کر رہا ہوں", lang)
        os.system("shutdown now")  # Linux shutdown command
    else:
        speak("Sorry, I can't do that yet." if lang == 'en' else "معاف کیجئے، میں یہ کام نہیں کر سکتا۔", lang)

# Main loop for Jarvis to listen and respond in Urdu or English
def jarvis():
    speak("Hello, how can I assist you today?" if recognizer.recognize_google_lang == 'en' else "سلام، میں آپ کی کس طرح مدد کر سکتا ہوں؟")
    while True:
        command, lang = take_command()
        if "exit" in command or "بند کرو" in command or "stop" in command:
            speak("Goodbye!" if lang == 'en' else "اللہ حافظ!", lang)
            break
        elif command != "None":
            execute_command(command, lang)

# Run the assistant
if __name__ == "__main__":
    jarvis()
