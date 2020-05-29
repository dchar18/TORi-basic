import tkinter as tk
from tkinter import *

# References:
# 1. multiple frames
#   - https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
#   - https://pythonprogramming.net/change-show-new-frame-tkinter/
#   - https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application
# 2. Escape/Toggle fullscreen
#   - https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/


LARGE_FONT = ("Verdana", 12)


def close():
    global root
    root.quit()


class TORiClass(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container["bg"] = "black"
        self.attributes("-fullscreen", True)
        self.fullScreenState = False
        self.bind("<Escape>", self.quitFullScreen)
        self["background"] = "black"

        # create a list of frames to choose from based on what action is chosen
        self.frames = {}

        for F in (MainView, Clock, Test):
            frame = F(container, self)  # F(parent=container, controller=self)
            frame["background"] = "black"
            self.frames[F] = frame
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame(MainView)
        # container.bind("<Button-1>", close)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.attributes("-fullscreen", self.fullScreenState)


class MainView(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main View", font=LARGE_FONT)
        label.pack(pady=5, padx=5, side=tk.TOP)
        # label.grid(column=0, row=0)

        button1 = tk.Button(self, text="Clock",
                            command=lambda: controller.show_frame(Clock),
                            height=2, width=40,
                            fg="blue",
                            bg="black")
        button1.pack()

        button2 = tk.Button(self, text="Test",
                            command=lambda: controller.show_frame(Test),
                            height=10, width=40,
                            fg="blue",
                            bg="black")
        button2.pack()


class Clock(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        clock = Label(root,
                      font=("times", 200, "bold"),
                      foreground="lightblue",
                      background="black")
        clock.pack()

        button1 = Button(self, text="Main", command=lambda: controller.show_frame(MainView))
        button1.pack()

        button2 = Button(self, text="Test", command=lambda: controller.show_frame(Test))
        button2.pack()



class Test(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Test View", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Main", command=lambda: controller.show_frame(MainView))
        button1.pack()

        button2 = Button(self, text="Clock", command=lambda: controller.show_frame(Clock))
        button2.pack()


app = TORiClass()
app.mainloop()