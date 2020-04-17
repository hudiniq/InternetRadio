import os
import pathlib
current_folder = pathlib.Path(__file__).parent.absolute()
os.add_dll_directory(str(current_folder) + "\\VLC")
import tkinter as tk
from PIL import Image, ImageTk
import vlc
import time
import harvester as H

root = tk.Tk()
root.geometry("600x70")
root.resizable(0, 0)

canvas = tk.Canvas(root, height = 70, width = 600)
canvas.pack()

url = "http://212.30.80.195:9034/rock"
#url = "http://145.14.14.93:9034/rock"
state = True
play_img = ImageTk.PhotoImage(file="play.png")
pause_img = ImageTk.PhotoImage(file="pause.png")
play_button = None
cover = None
song = None
vol = None

instance = vlc.Instance()
media=instance.media_new(url)
player=instance.media_player_new()
player.set_media(media)


def main():
    global play_button, cover, song, vol

    H.fetch()
    
    play_button = tk.Button(canvas, image = play_img, command = play_pause)
    play_button.place(relx = 0, rely = 0, relwidth = 0.20, relheight = 1)

    img = ImageTk.PhotoImage(Image.open(H.fetch_img()).resize((84, 70), Image.ANTIALIAS))
    cover = tk.Label(canvas, image = img)
    cover.place(relx = 0.20, relwidth = 0.14, relheight = 1)

    song = tk.Label(canvas, text = H.fetch_song())
    song.place(relx = 0.34, relwidth = 0.51, relheight = 1)

    # refresh_button = tk.Button(canvas, text = "refresh", command = refresher)
    # refresh_button.place(relx = 0.85, relwidth = 0.10, relheight = 1)

    vol = tk.Scale(canvas, from_ = 100, to = 0, command=set_volume)
    vol.set(100)
    vol.place(relx = 0.93, relwidth = 0.5, relheight = 1)

    root.mainloop()
    H.kill()


def play_pause():
    global play_button
    global state
    if state is True:
        state = False
        play_button.configure(image=pause_img)
        player.play()
    else:
        state = True
        play_button.configure(image=play_img)
        player.pause()

def set_volume(v):
    global vol
    value = vol.get()
    player.audio_set_volume(value)

# def refresher():
    # global cover, song
    # img = ImageTk.PhotoImage(Image.open(H.fetch_img()).resize((84, 70), Image.ANTIALIAS))

    # cover.configure(image = img)
    # song.configure(text = H.fetch_song())
    
    # root.after(1000, refresher())


if __name__ == "__main__":
    main()