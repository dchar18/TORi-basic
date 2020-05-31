import tkinter as tk
import time
from datetime import date
import sys
import os
import subprocess

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
months = {1: "January", 2: "February",
          3: "March", 4: "April",
          5: "May", 6: "June",
          7: "July", 8: "August",
          9: "September", 10: "October",
          11: "November", 12: "December"}


def close():
    global root
    root.quit()


def beep():
    duration = 0.3  # seconds
    freq = 1046.50  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


# taken from Reference 1.a
# used as a template to initialize each frame
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class CentralView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(
            self,
            text="Main View",
            font=LARGE_FONT
        )
        label.pack(side="top", fill="both", expand=True)


class ClockView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.time_str = "00:00:00"  # from reference 3.a
        self.date_str = "January 1, 2000"  # default date
        self.time_label = tk.Label(
            self,
            text=self.time_str,
            fg="lightblue",
            bg="black",
            font=("times", 200, "bold")
        )
        self.time_label.pack(side="top", fill="both", expand=True)
        self.date_label = tk.Label(
            self,
            text=self.date_str,
            fg="white",
            bg="black",
            font=("times", 75, "bold")
        )
        self.date_label.pack(side="top", fill="both", expand=True)
        self.time_label.after(1000, self.timeTick)

    # from reference 3.a
    def timeTick(self):
        # get updated time
        self.time_str = time.strftime("%H:%M:%S")
        # get updated date
        date_today = date.today()
        self.date_str = months[date_today.month] + " " + str(date_today.day) + ", " + str(date_today.year)
        # update the labels
        self.time_label.config(text=self.time_str)
        self.date_label.config(text=self.date_str)
        # wait a second to update the date/time again
        self.time_label.after(1000, self.timeTick)


class PomodoroTimerView(Page):
    minutes = 25
    seconds = 0
    interval = 0  # 0 = study time (25 minutes), 1 = break time (5 minutes)
    num_study_passed = 0  # stores the number of study periods that have passed
    num_break_passed = 0
    paused = False  # keeps track of whether the pause button was pressed

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        # timer attributes -----------------------------------------------
        self.timer_str = '{:02d}:{:02d}'.format(self.minutes, self.seconds)
        self.time_label = tk.Label(
            self,
            text=self.timer_str,
            font=("times", 175, "bold"),
        )
        self.time_label.pack(side="top", fill="both", expand=True)

        # buttons (start, pause, reset) ----------------------------------
        button_frame = tk.Frame(self, bg="black", height=40)
        button_frame.pack(side="top", fill="x", expand=False)
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            fg="black",
            bg="lightgreen",
            height=5,
            command=self.startTimer
        )
        self.start_button.pack(side="top", fill="both", expand=True)

        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            fg="black",
            bg="red",
            height=5,
            command=self.pauseTimer
        )
        self.pause_button.pack(side="top", fill="both", expand=True)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            fg="black",
            bg="lightblue",
            height=5,
            command=self.resetTimer
        )

    def startTimer(self):
        self.start_button.grid_forget()
        self.reset_button.pack(side="top", fill="both", expand=True)

        if not self.paused:
            # XX:00
            if self.seconds == 0:
                # 00:00
                if self.minutes == 0:
                    # study time is over
                    if self.interval == 0:
                        # BEEP (of some notification) - TODO
                        # beep()
                        os.system('spd-say "break time"')
                        # 5 minutes of break time have begun
                        self.minutes = 4
                        self.seconds = 59
                        self.interval = 1
                    # break time is over
                    else:
                        # BEEP (of some notification) - TODO
                        # sys.stdout.write('\a')
                        os.system('spd-say "work time"')
                        # beep()
                        # 25 minutes of study time have begun
                        self.minutes = 24
                        self.seconds = 59
                        self.interval = 0
                # a minute has passed and time still remains
                else:
                    self.minutes -= 1
                    self.seconds = 59
            # seconds > 0
            else:
                self.seconds -= 1
            self.timer_str = '{:02d}:{:02d}'.format(self.minutes, self.seconds)
            self.time_label.config(text=self.timer_str)
        self.time_label.after(1000, self.startTimer)
        # self.reset_button.grid_forget()
        # self.start_button.grid()

    def pauseTimer(self):
        if self.paused:
            self.paused = False
            self.pause_button.config(text="Pause")
        else:
            self.paused = True
            self.pause_button.config(text="Continue")

    def resetTimer(self):
        self.minutes = 25
        self.seconds = 0
        self.interval = 0  # 0 = study time (25 minutes), 1 = break time (5 minutes)
        self.num_study_passed = 0
        self.num_break_passed = 0
        self.paused = False
        self.pause_button.config(text="Pause")


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        v1 = CentralView(self)
        v1["bg"] = "black"
        v2 = ClockView(self)
        v2["bg"] = "black"
        v3 = PomodoroTimerView(self)
        v3["bg"] = "black"

        button_frame = tk.Frame(self, bg="black")
        container = tk.Frame(self, bg="black")
        button_frame.pack(side="right", fill="x", expand=False)
        container.pack(side="left", fill="both", expand=True)

        v1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        v2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        v3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # button for main screen
        b1 = tk.Button(
            button_frame,
            text="Main View",
            fg="white",
            bg="gray",
            width=15,
            height=10,
            command=v1.lift
        )
        # button for Clock screen (TEMPORARY)
        b2 = tk.Button(
            button_frame,
            text="Clock",
            fg="white",
            bg="gray",
            width=15,
            height=10,
            command=v2.lift
        )
        # button for Pomodoro Timer screen
        b3 = tk.Button(
            button_frame,
            text="Pomodoro \nTimer",
            fg="white",
            bg="gray",
            width=15,
            height=10,
            command=v3.lift
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
        exit_button.pack(side="top")

        v1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main["background"] = "black"
    main.pack(side="top", fill="both", expand=True)
    # root.wm_geometry("400x400")
    root.attributes("-fullscreen", True)
    root.mainloop()
