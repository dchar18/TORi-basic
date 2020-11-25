import tkinter as tk
from time import sleep
from picamera import PiCamera

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class CameraView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        button_frame = tk.Frame(
            self,
            bg="blue",
        )
        button_frame.pack(side="top", fill="x", expand=False)

        self.camera_short_button = tk.Button(
            button_frame,
            text="Open Camera short",
            font=("times", 25, "bold"),
            fg="black",
            bg="blue",
            height=4,
            command=self.startCameraShort
        )
        self.camera_short_button.pack(side="top", fill="both", expand=True)

        self.camera_med_button = tk.Button(
            button_frame,
            text="Open Camera medium",
            font=("times", 25, "bold"),
            fg="black",
            bg="blue",
            height=4,
            command=self.startCameraMed
        )
        self.camera_med_button.pack(side="top", fill="both", expand=True)

        self.camera_long_button = tk.Button(
            button_frame,
            text="Open Camera long",
            font=("times", 25, "bold"),
            fg="black",
            bg="blue",
            height=4,
            command=self.startCameraLong
        )
        self.camera_long_button.pack(side="top", fill="both", expand=True)


    def startCameraShort(self):
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(5)
        self.camera.stop_preview()
        del self.camera

    def startCameraMed(self):
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(10)
        self.camera.stop_preview()
        del self.camera

    def startCameraLong(self):
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(15)
        self.camera.stop_preview()
        del self.camera