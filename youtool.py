import tkinter as tk
import requests
from pytube import YouTube
import os
import crayons


video_directory = "./Videos"
thumbnail_directory = "./Thumbnails"

if not os.path.exists(video_directory):
    os.makedirs(video_directory)

if not os.path.exists(thumbnail_directory):
    os.makedirs(thumbnail_directory)

def download_youtube_video():
    url = link_input_video.get()
    if url:
        try:
            yt = YouTube(url)
            title = yt.title
            yt.streams.filter(progressive=True, file_extension='mp4')
            yt.streams.get_highest_resolution().download(output_path=video_directory)
            log_message.set("Successfully downloaded: " + str(title))
            print(crayons.green("Successfully downloaded: " + str(title)))
        except Exception as e:
            log_message.set(f"An error occurred: {e}")

def download_youtube_thumbnail():
    url = link_input.get()
    if url:
        try:
            yt = YouTube(url)
            title = yt.title
            img_url = yt.thumbnail_url
            content =  requests.get(img_url).content
            minia = open(thumbnail_directory + "/" + title + ".png", "wb")
            minia.write(content)
            minia.close()
            log_message.set("Successfully downloaded: " + str(title) + ".png")
            print(crayons.green("Successfully downloaded: " + str(title) + ".png"))
        except Exception as e:
            log_message.set(f"An error occurred: {e}")

root = tk.Tk()

root.title("YouTool")
root.geometry("600x400")

label = tk.Label(root, text="YouTool", font=("Arial", 20))
label.pack()

#Download Video Method
label = tk.Label(root, text="Download Video", font=("Arial", 12))
label.pack()

link_input_video = tk.Entry(root)
link_input_video.pack()

download_button = tk.Button(root, text="Download", command=download_youtube_video)
download_button.pack(pady=2)

#Download Thumbnail
label = tk.Label(root, text="Download Thumbnail", font=("Arial", 12))
label.pack()

link_input = tk.Entry(root)
link_input.pack()

download_button = tk.Button(root, text="Download", command=download_youtube_thumbnail)
download_button.pack(pady=2)

#Extre
log_message = tk.StringVar()
error_label = tk.Label(root, textvariable=log_message)
error_label.pack(pady=5)


download_button = tk.Button(root, text="@GaelHF")
download_button.pack(pady=5)

root.mainloop()