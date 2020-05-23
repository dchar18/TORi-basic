import tkinter as tk
from tkinter import *

LARGE_FONT = ("Verdana", 12)


class TORiClass(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainView, Clock, Test):
            frame = F(container, self)  # F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame(MainView)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainView(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main View", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Clock", command=lambda: controller.show_frame(Clock))
        button1.pack()

        button2 = Button(self, text="Test", command=lambda: controller.show_frame(Test))
        button2.pack()


class Clock(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Clock View", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

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
