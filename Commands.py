import ascii_magic
import crayons
import os
from Clippy import speak
from win10toast import ToastNotifier

def url_to_ascii(link):
    url = link
    if url:
        try:
            ascii_image = ascii_magic.from_url(url)
            ascii_image.to_terminal(columns=200)
            print(crayons.cyan("Converted image to ASCII"))
            speak("Converted image to ASCII")
        except Exception as e:
            print(crayons.red(f"Error {e}"))
    else:
        print(crayons.red("Please mention a valid url !"))
        speak("Please mention a valid url !")

def open_youtool():
    if os.path.exists('youtool.py'):
        print(crayons.green("Opening YouTool..."))
        os.system(f"python youtool.py")
    else:
        print(crayons.red("YouTool is not installed"))
        print(crayons.cyan("You can install it at: https://github.com/GaelHF/YouTool"))
        speak("YouTool is not installed")

def talk_to_an_ai():
    print(crayons.cyan("I don't have an AI yet so I suggest you talk with these AIs:"))
    print(crayons.blue("https://chat.openai.com/"))
    print(crayons.blue("https://blackbox.chat/"))
    speak("I don't have an AI yet so I suggest you to talk with these AI")

def help():
    print(crayons.cyan("My commands are : "))
    print(crayons.blue("   - Prefix: Clippy"))
    print(crayons.blue("   - Clippy image to letters (ASCII ART)"))
    print(crayons.blue("   - Clippy download youtube (Opens YouTool)"))
    print(crayons.blue("   - Clippy talk (AI)"))
    print(crayons.blue("   - Clippy clock (Creates timer)"))
    print(crayons.blue("   - Clippy go to [url] (Opens web page)"))
    print(crayons.blue("   - Clippy search for [search] (Make a Google Research)"))
    print(crayons.blue("   - Clippy help (displays commands)"))
    print(crayons.blue("   - Clippy hello / hi (Say Hello To Clippy)"))
    print(crayons.blue("   - Clippy quit / exit / leave / goodbye (Quits Clippy)"))