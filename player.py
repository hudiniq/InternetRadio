import os
import pathlib
current_folder = pathlib.Path(__file__).parent.absolute()
os.add_dll_directory(str(current_folder) + "\\VLC")
import tkinter as tk
from PIL import Image, ImageTk
import vlc
import time
import threading
import harvester


class InternetRadio():
    def __init__(self, root):
        self.root = root
        self.root.wm_title("ROCK RADIO")
        self.root.geometry("600x70")
        self.root.resizable(0, 0)

        self.canvas = tk.Canvas(self.root, height = 70, width = 600)
        self.canvas.pack()

        self.url = "http://212.30.80.195:9034/rock"
        #self.url = "http://145.14.14.93:9034/rock"
        self.state = True
        self.play_img = ImageTk.PhotoImage(file="play.png")
        self.pause_img = ImageTk.PhotoImage(file="pause.png")

        self.instance = vlc.Instance()
        self.media=self.instance.media_new(self.url)
        self.player=self.instance.media_player_new()
        self.player.set_media(self.media)

        self.draw()


    def draw(self):
        self.play_button = tk.Button(self.canvas, image = self.play_img, command = self.play_pause)
        self.play_button.place(relx = 0, rely = 0, relwidth = 0.20, relheight = 1)

        self.cover = tk.Label(self.canvas, image = None)
        self.cover.place(relx = 0.20, relwidth = 0.14, relheight = 1)

        self.song = tk.Label(self.canvas, text = "Fetching Data...")
        self.song.place(relx = 0.34, relwidth = 0.61, relheight = 1)

        self.vol = tk.Scale(self.canvas, from_ = 100, to = 0, command=self.set_volume)
        self.vol.set(100)
        self.vol.place(relx = 0.93, relwidth = 0.5, relheight = 1)

        self.root.after(1000, self.start_refresher)

    def play_pause(self):
        if self.state is True:
            self.state = False
            self.play_button.configure(image=self.pause_img)
            self.player.play()
        else:
            self.state = True
            self.play_button.configure(image=self.play_img)
            self.player.pause()

    def set_volume(self, v):
        value = self.vol.get()
        self.player.audio_set_volume(value)

    def start_refresher(self):
        self.H = harvester.Harvester()
        self.refresher()

    def refresher(self):
        self.img = ImageTk.PhotoImage(Image.open(self.H.fetch_img()).resize((84, 70), Image.ANTIALIAS))
        self.cover.place(relx = 0.20, relwidth = 0.14, relheight = 1)

        self.cover.configure(image = self.img)
        self.song.configure(text = self.H.fetch_song())
        
        self.root.after(10000, self.refresher)


if __name__ == "__main__":
    root = tk.Tk()
    app = InternetRadio(root)
    root.mainloop()
    app.player.stop()
    app.H.kill()
