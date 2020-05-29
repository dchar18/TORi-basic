import tkinter as tk
import time

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


def close():
    global root
    root.quit()


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
        label = tk.Label(self, text="Main View", font=LARGE_FONT)
        label.pack(side="top", fill="both", expand=True)


class ClockView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.time_str = "00:00:00"  # from reference 3.a
        self.time_label = tk.Label(self, text=self.time_str, fg="lightblue", bg="black", font=("times", 200, "bold"))
        self.time_label.pack(side="top", fill="both", expand=True)
        self.time_label.after(1000, self.timeTick)

    # from reference 3.a
    def timeTick(self):
        self.time_str = time.strftime("%H:%M:%S")
        self.time_label.config(text=self.time_str)
        self.time_label.after(1000, self.timeTick)


class TestView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Test View", font=LARGE_FONT)
        label.pack(side="top", fill="both", expand=True)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.v2 = ClockView
        v1 = CentralView(self)
        v1["bg"] = "black"
        v2 = ClockView(self)
        v2["bg"] = "black"
        v3 = TestView(self)
        v3["bg"] = "black"

        button_frame = tk.Frame(self)
        container = tk.Frame(self)
        button_frame.pack(side="right", fill="x", expand=False)
        container.pack(side="left", fill="both", expand=True)

        v1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        v2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        v3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(
            button_frame,
            text="Main View",
            fg="white",
            bg="black",
            width=10,
            height=10,
            command=v1.lift
        )
        b2 = tk.Button(
            button_frame,
            text="Clock",
            fg="white",
            bg="black",
            width=10,
            height=10,
            command=v2.lift
        )
        b3 = tk.Button(
            button_frame,
            text="Test",
            fg="white",
            bg="black",
            width=10,
            height=10,
            command=v3.lift
        )
        exit_button = tk.Button(
            button_frame,
            text="Exit",
            bg="red",
            width=10,
            height=10,
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
    main.pack(side="top", fill="both", expand=True)
    # root.wm_geometry("400x400")
    root.attributes("-fullscreen", True)
    root.mainloop()
