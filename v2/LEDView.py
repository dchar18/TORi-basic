import tkinter as tk
from gpiozero import LED
from time import sleep

# floor 1 pins
floor1_led1 = LED(17)  # floor 1 led pin 1
floor1_led2 = LED(27)  # floor 1 led pin 2
floor1_led3 = LED(22)  # floor 1 led pin 3
# floor 2 pins
floor2_led1 = LED(5)  # floor 2 led pin 1
floor2_led2 = LED(6)  # floor 2 led pin 2
floor2_led3 = LED(26)  # floor 2 led pin 3
# floor 3 pins
floor3_led1 = LED(23)  # floor 3 led pin 1
floor3_led2 = LED(24)  # floor 3 led pin 2
floor3_led3 = LED(25)  # floor 3 led pin 3 (rightmost)
# floor 4 pins 
floor4_led1 = LED(14)  # floor 4 led pin 1
floor4_led2 = LED(15)  # floor 4 led pin 2
floor4_led3 = LED(18)  # floor 4 led pin 3


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class LEDView(Page):
    floor1_on = False
    floor2_on = False
    floor3_on = False
    floor4_on = False

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        button_frame = tk.Frame(
            self,
            bg="blue",
        )
        button_frame.pack(side="top", fill="x", expand=False)

        # floor 4 setup
        self.floor4_button = tk.Button(
            button_frame,
            text="Floor 4: OFF",
            font=("times", 25, "bold"),
            fg="black",
            bg="red",
            height=4,
            command=self.changeFloor4State
        )
        self.floor4_button.pack(side="top", fill="both", expand=True)

        # floor 3 setup
        self.floor3_button = tk.Button(
            button_frame,
            text="Floor 3: OFF",
            font=("times", 25, "bold"),
            fg="black",
            bg="red",
            height=4,
            command=self.changeFloor3State
        )
        self.floor3_button.pack(side="top", fill="both", expand=True)

        # floor 2 setup
        self.floor2_button = tk.Button(
            button_frame,
            text="Floor 2: OFF",
            font=("times", 25, "bold"),
            fg="black",
            bg="red",
            height=4,
            command=self.changeFloor2State
        )
        self.floor2_button.pack(side="top", fill="both", expand=True)

        # floor 1 setup
        self.floor1_button = tk.Button(
            button_frame,
            text="Floor 1: OFF",
            font=("times", 25, "bold"),
            fg="black",
            bg="red",
            height=4,
            command=self.changeFloor1State
        )
        self.floor1_button.pack(side="top", fill="both", expand=True)

        self.allfloor_button = tk.Button(
            button_frame,
            text="All Floors: OFF",
            font=("times", 25, "bold"),
            fg="black",
            bg="red",
            height=2,
            command=self.changeAllFloor
        )
        self.allfloor_button.pack(side="top", fill="both", expand=True)

    def changeFloor4State(self):
        self.floor4_on = not self.floor4_on

        if self.floor4_on:  # LEDs are now on
            floor4_led1.on()
            floor4_led2.on()
            floor4_led3.on()
            self.floor4_button["bg"] = "lightgreen"
            self.floor4_button["text"] = "Floor 4: ON"
        else:  # LEDs are now off
            floor4_led1.off()
            floor4_led2.off()
            floor4_led3.off()
            self.floor4_button["bg"] = "red"
            self.floor4_button["text"] = "Floor 4: OFF"

    def changeFloor3State(self):
        self.floor3_on = not self.floor3_on

        if self.floor3_on:  # LEDs are now on
            floor3_led1.on()
            floor3_led2.on()
            floor3_led3.on()
            self.floor3_button["bg"] = "lightgreen"
            self.floor3_button["text"] = "Floor 3: ON"
        else:  # LEDs are now off
            floor3_led1.off()
            floor3_led2.off()
            floor3_led3.off()
            self.floor3_button["bg"] = "red"
            self.floor3_button["text"] = "Floor 3: OFF"

    def changeFloor2State(self):
        self.floor2_on = not self.floor2_on

        if self.floor2_on:  # LEDs are now on
            floor2_led1.on()
            floor2_led2.on()
            floor2_led3.on()
            self.floor2_button["bg"] = "lightgreen"
            self.floor2_button["text"] = "Floor 2: ON"
        else:  # LEDs are now off
            floor2_led1.off()
            floor2_led2.off()
            floor2_led3.off()
            self.floor2_button["bg"] = "red"
            self.floor2_button["text"] = "Floor 2: OFF"

    def changeFloor1State(self):
        self.floor1_on = not self.floor1_on

        if self.floor1_on:  # LEDs are now on
            floor1_led1.on()
            floor1_led2.on()
            floor1_led3.on()
            self.floor1_button["bg"] = "lightgreen"
            self.floor1_button["text"] = "Floor 1: ON"
        else:  # LEDs are now off
            floor1_led1.off()
            floor1_led2.off()
            floor1_led3.off()
            self.floor1_button["bg"] = "red"
            self.floor1_button["text"] = "Floor 1: OFF"

    def changeAllFloor(self):
        if self.floor1_on or self.floor2_on or self.floor3_on or self.floor4_on:
            floor1_led1.off()
            floor1_led2.off()
            floor1_led3.off()
            floor2_led1.off()
            floor2_led2.off()
            floor2_led3.off()
            floor3_led1.off()
            floor3_led2.off()
            floor3_led3.off()
            floor4_led1.off()
            floor4_led2.off()
            floor4_led3.off()
            self.floor1_button["bg"] = "red"
            self.floor1_button["text"] = "Floor 1: OFF"
            self.floor2_button["bg"] = "red"
            self.floor2_button["text"] = "Floor 2: OFF"
            self.floor3_button["bg"] = "red"
            self.floor3_button["text"] = "Floor 3: OFF"
            self.floor4_button["bg"] = "red"
            self.floor4_button["text"] = "Floor 4: OFF"
            self.allfloor_button["bg"] = "red"
            self.allfloor_button["text"] = "All Floors: OFF"

            self.floor1_on = False
            self.floor2_on = False
            self.floor3_on = False
            self.floor4_on = False
        else:
            floor1_led1.on()
            floor1_led2.on()
            floor1_led3.on()
            floor2_led1.on()
            floor2_led2.on()
            floor2_led3.on()
            floor3_led1.on()
            floor3_led2.on()
            floor3_led3.on()
            floor4_led1.on()
            floor4_led2.on()
            floor4_led3.on()
            self.floor1_button["bg"] = "lightgreen"
            self.floor1_button["text"] = "Floor 1: ON"
            self.floor2_button["bg"] = "lightgreen"
            self.floor2_button["text"] = "Floor 2: ON"
            self.floor3_button["bg"] = "lightgreen"
            self.floor3_button["text"] = "Floor 3: ON"
            self.floor4_button["bg"] = "lightgreen"
            self.floor4_button["text"] = "Floor 4: ON"
            self.allfloor_button["bg"] = "lightgreen"
            self.allfloor_button["text"] = "All Floors: ON"

            self.floor1_on = True
            self.floor2_on = True
            self.floor3_on = True
            self.floor4_on = True
