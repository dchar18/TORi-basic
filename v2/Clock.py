# Clock.py:
# - displays a running clock with the date
#
# OffClock:
# - displays a clock that appears after 10 seconds of inactivity
#
# ClockView:
# - displays the ClockView Frame when Clock button is pressed
import tkinter as tk
import time
from datetime import date

months = {1: "January", 2: "February",
          3: "March", 4: "April",
          5: "May", 6: "June",
          7: "July", 8: "August",
          9: "September", 10: "October",
          11: "November", 12: "December"}


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


# This code works as a stand-alone clock ---------------------------------
class OffClock(Page):
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

# root = Tk()
# root.attributes("-fullscreen", True)
# root["background"] = "black"
# clock = Label(root,
#               font=("times", 200, "bold"),
#               foreground="lightblue",
#               background="black")
# clock.grid(column=0, row=0)
#
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
# root.bind("<Button-1>", close)
# tick()
# root.mainloop()
# ------------------------------------------------------------------------


# this class is used as a place-holder that will be substituted with OffClock
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
