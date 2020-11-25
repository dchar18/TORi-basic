# Main.py:
# - main project file
# - creates all views as well as the buttons that navigate the views
import tkinter as tk
import time
from datetime import date
import sys
import os
import subprocess
import threading
from Clock import ClockView, OffClock
from Pomodoro import PomodoroTimerView
from Spotify import SpotifyView
from LEDView import LEDView
from CameraView import CameraView
# References:
# 1. multiple frames
#   a. https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
#   b. https://pythonprogramming.net/change-show-new-frame-tkinter/
#   c. https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application
# 2. Escape/Toggle fullscreen
#   a. https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/
# 3. Clock functionality
#   a. https://riptutorial.com/tkinter/example/22870/-after--

LARGE_FONT = ("Verdana", 12)
counter = 0  # global variable that keeps track of how many seconds have passed since the last action
recent_frame = -1  # keeps track of what frame was displayed before screen time-out


def close():
    global root
    root.quit()


def beep():
    duration = 0.3  # seconds
    freq = 1046.50  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


def changeFrame(self):
    counter = 0
    self.lift()


def resetInteractionTimer():
    counter = 0


def checkInteraction():
    if counter == 10:
        changeFrame(Views.frames[1])
        timer.start()
    # else:
    #     timer.start()


# taken from Reference 1.a
# used as a template to initialize each frame
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class MainView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(
            self,
            text="Main View",
            font=LARGE_FONT
        )
        label.pack(side="top", fill="both", expand=True)


class Views(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        v1 = MainView(self)
        v1["bg"] = "black"
        v2 = ClockView(self)
        v2["bg"] = "black"
        v3 = PomodoroTimerView(self)
        v3["bg"] = "black"
        v4 = SpotifyView(self)
        v4["bg"] = "black"
        # v5 = LEDView(self)
        # v5["bg"] = "black"
        v5 = CameraView(self)
        v5['bg'] = 'black'
        self.frames = {v1, v2, v3, v4, v5}
        # off = OffClock(self)
        # off["bg"] = "black"

        button_frame = tk.Frame(self, bg="black")
        container = tk.Frame(self, bg="black")
        button_frame.pack(side="right", fill="x", expand=False)
        container.pack(side="left", fill="both", expand=True)

        v1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        v2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        v3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        v4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        v5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        # off.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # button for main screen
        b1 = tk.Button(
            button_frame,
            text="Main View",
            fg="white",
            bg="gray",
            width=15,
            height=7,
            command=lambda: changeFrame(v1)
        )
        # button for Clock screen (TEMPORARY)
        b2 = tk.Button(
            button_frame,
            text="Clock",
            fg="white",
            bg="gray",
            width=15,
            height=7,
            command=lambda: changeFrame(v2)
        )
        # button for Pomodoro Timer screen
        b3 = tk.Button(
            button_frame,
            text="Pomodoro \nTimer",
            fg="white",
            bg="gray",
            width=15,
            height=7,
            command=lambda: changeFrame(v3)
        )
        b4 = tk.Button(
            button_frame,
            text="Spotify",
            fg="white",
            bg="gray",
            width=15,
            height=7,
            command=lambda: changeFrame(v4)
        )
        b5 = tk.Button(
            button_frame,
            text="Camera",
            fg="white",
            bg="gray",
            width=15,
            height=7,
            command=lambda: changeFrame(v5)
        )
        exit_button = tk.Button(
            button_frame,
            text="Exit",
            bg="red",
            width=15,
            height=5,
            command=close
        )

        b1.pack(side="top")
        b2.pack(side="top")
        b3.pack(side="top")
        b4.pack(side="top")
        b5.pack(side="top")
        exit_button.pack(side="top")

        v1.show()

    def getFrame(self, i):
        return self.frames[i]


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    main = Views(root)
    main["background"] = "black"
    main.pack(side="top", fill="both", expand=True)
    timer = threading.Timer(10.0, checkInteraction)
    timer.start()
    root.mainloop()
