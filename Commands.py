import ascii_magic
import crayons
import os
from Clippy import speak

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