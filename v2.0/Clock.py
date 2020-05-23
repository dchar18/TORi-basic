from tkinter import *
from time import gmtime, strftime
from datetime import datetime
import time
import sys


def tick():
    time_str = time.strftime("%H:%M:%S")
    clock.config(text=time_str)
    clock.after(200, tick)


def close(event):
    global root
    root.quit()


root = Tk()
root.attributes("-fullscreen", True)
root["background"] = "black"
clock = Label(root,
              font=("times", 200, "bold"),
              foreground="lightblue",
              background="black")
clock.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.bind("<Button-1>", close)
tick()
root.mainloop()