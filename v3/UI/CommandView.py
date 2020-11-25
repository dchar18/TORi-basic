import tkinter as tk
from time import sleep

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class CommandView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        button_frame = tk.Frame(
            self,
            bg="blue",
        )
        button_frame.pack(side="top", fill="x", expand=False)