# CentralView.py:
# - serves as the main view of the application
import tkinter as tk

LARGE_FONT = ("Verdana", 12)


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


