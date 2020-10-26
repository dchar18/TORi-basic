import tkinter as tk
import os


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


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
            bg="orange"
        )
        self.time_label.pack(side="top", fill="both", expand=True)

        # buttons (start, pause, reset) ----------------------------------
        button_frame = tk.Frame(
            self,
            bg="black",
            height=40
        )
        button_frame.pack(side="top", fill="x", expand=False)
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            font=("times", 25, "bold"),
            fg="black",
            bg="lightgreen",
            height=2,
            command=self.startTimer
        )
        self.start_button.pack(side="left", fill="both", expand=True)

        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            font=("times", 25, "bold"),
            fg="black",
            bg="red",
            height=2,
            command=self.pauseTimer
        )
        self.pause_button.pack(side="left", fill="both", expand=True)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            font=("times", 25, "bold"),
            fg="black",
            bg="lightblue",
            height=2,
            command=self.resetTimer
        )

    def startTimer(self):
        self.start_button.grid_forget()
        self.reset_button.pack(side="left", fill="both", expand=True)

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