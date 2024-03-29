import pyttsx3
import speech_recognition as sr
import google.cloud.texttospeech as tts
from ctypes import *
from contextlib import contextmanager
import pygame
import time
import math
import Commands
import crayons
import webbrowser
import ascii_magic
import os
import threading
from win10toast import ToastNotifier
import config

def timer(seconds):
    time.sleep(seconds)
    print(crayons.blue("TIME IS UP !"))
    notif = ToastNotifier()
    speak("TIME IS UP !")
    notif.show_toast('Clippy', 'Your Timer is Done', icon_path='./clippy.ico', duration=3)

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    try: 
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except:
        yield
        print('')

### PARAMETERS ###
#Browser
webbrowser.register('web', None, webbrowser.BackgroundBrowser(config.browser_path))

activationWords = config.activate_names
tts_type = 'local'

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[config.Voice].id) # 0=Homme,1=Femme

# Google TTS client
def google_text_to_wav(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])

    # Set the text input to be synthesized
    text_input = tts.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the voice name
    voice_params = tts.VoiceSelectionParams(
        language_code='en-CA', name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    return response.audio_content

def parseCommand():
    with noalsaerr():
        listener = sr.Recognizer()
        print(crayons.cyan('Waiting for a command...'))

        with sr.Microphone() as source:
            listener.pause_threshold = 2
            input_speech = listener.listen(source)

        try:
            print(crayons.cyan('Loading...'))
            query = listener.recognize_google(input_speech, language='en_US')
            query2 = str(query).replace("clippy", 'Clippy')
            query3 = query2.replace("creepy", 'Clippy')
            query4 = query3.replace("sleepy", 'Clippy')
            print(crayons.cyan(f'Your command: {query4}'))

        except Exception as exception:
            print(crayons.cyan("I didn't understand please repeat."))
            print(crayons.red(exception))

            return 'None'

        return query

def speak(text, rate = 120):
    time.sleep(0.3)
    try:     
        if tts_type == 'local':
            engine.setProperty('rate', rate) 
            engine.say(text, 'txt')
            engine.runAndWait()
        if tts_type == 'google':
            speech = google_text_to_wav('en-CA', text)
            pygame.mixer.init(frequency=12000, buffer = 512)
            speech_sound = pygame.mixer.Sound(speech)
            speech_length = int(math.ceil(pygame.mixer.Sound.get_length(speech_sound)))
            speech_sound.play()
            time.sleep(speech_length)
            pygame.mixer.quit()
 
    ## The standard keyboard interrupt is Ctrl+C. This interrupts the Google speech synthesis.
    except KeyboardInterrupt:
        try:
            if tts_type == 'google':
                pygame.mixer.quit()
        except:
            pass
        return
    
if __name__ == '__main__':
    print(crayons.yellow("Clippy coded by: @GaelHF"))
    print(crayons.blue("My GitHub: https://github.com/GaelHF"))
    if os.path.exists('./clippy.png'):
        clippy = ascii_magic.from_image('./clippy.png')
        clippy.to_terminal(columns=60)
    print(crayons.cyan('Hello Human, Clippy is here !'))
    speak('Hello Human, Clippy is here !')

    while True:
        query = parseCommand().lower().split()
        if query[0] in activationWords:
            query[0] = 'clippy'
        if query[0] == 'clippy' and len(query) > 1:
            query.pop(0)

            #HELP
            if query[0] == "help":
                Commands.help()

            if query[0] in config.commandhandler:
                command = config.commandhandler[query[0]]
                command()

            #ASCII ART
            if query[0] == 'image' and query[1] == 'to' and query[2] == 'letters':
                lien = input('Image URL : ')
                if lien:
                    Commands.url_to_ascii(lien)
                else:
                    print(crayons.red("Error: Please enter a valid URL !"))
            if query[0] == 'smash':
                Commands.smash()

            # Web
            if query[0] == 'go' and query[1] == 'to':
                print(crayons.cyan('Opening...'))
                speak('Opening... ')
                query = ' '.join(query[2:])
                webbrowser.get('web').open_new(query)

            if query[0] == 'search' and query[1] == 'for':
                print(crayons.cyan('Opening...'))
                speak('Opening... ')
                query = ' '.join(query[2:])
                webbrowser.get('web').open_new("https://www.google.com/search?&q="+query)

            #YouTool
            if query[0] == "download" and query[1] == "youtube":
                Commands.open_youtool()

            #Terravision
            if query[0] == "map":
                Commands.map()

            #AI
            if query[0] == "talk":
                Commands.talk_to_an_ai()

            #Clock
            if query[0] == "clock":
                mins = input('Minutes : ')
                if mins:
                    sec = float(mins) * 60
                    timer_thread = threading.Thread(target=timer, args=(sec,))
                    timer_thread.start()
                else:
                    print(crayons.cyan("Please put a valid number of minutes."))
                    speak("Please put a valid number of minutes.")


            #Conversation
            if query[0] == 'hello' or query[0] == 'hi':
                print(crayons.cyan("Hello Human"))
                speak('Hello Human')

            #QUIT
            if query[0] == 'quit' or query[0] == 'exit' or query[0] == 'leave' or query[0] == 'goodbye':
                print(crayons.cyan("Good bye Human, see you next time !"))
                speak("Good bye Human, see you next time !")
                break