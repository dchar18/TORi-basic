import tkinter as tk
from gpiozero import LED
from time import sleep

floor1_led = LED(17) # floor 1 led pin
floor2_led = LED(27) # floor 2 led pin
floor3_led = LED(22) # floor 3 led pin
floor4_led = LED(10) # floor 4 led pin
topfloor_led = LED(9) # top floor led pin

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
	topfloor_on = False

	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)

		button_frame = tk.Frame(
			self,
			bg="blue",
		)
		button_frame.pack(side="top", fill="x", expand=False)

		# top floor button setup
		self.topfloor_button = tk.Button(
			button_frame,
			text="Top: OFF",
			font=("times", 25, "bold"),
			fg="black",
			bg="red",
			height=3,
			command=self.changeTopFloorState
        )
		self.topfloor_button.pack(side="top", fill="both", expand=True)

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

	def changeTopFloorState(self):
		self.topfloor_on = not self.topfloor_on

		if self.topfloor_on: # LEDs are now on
			topfloor_led.on()
			self.topfloor_button["bg"] = "lightgreen"
			self.topfloor_button["text"] = "Top: ON"
		else: # LEDs are now off
			topfloor_led.off()
			self.topfloor_button["bg"] = "red"
			self.topfloor_button["text"] = "Top: OFF"

	def changeFloor4State(self):
		self.floor4_on = not self.floor4_on

		if self.floor4_on: # LEDs are now on
			floor4_led.on()
			self.floor4_button["bg"] = "lightgreen"
			self.floor4_button["text"] = "Floor 4: ON"
		else: # LEDs are now off
			floor4_led.off()
			self.floor4_button["bg"] = "red"
			self.floor4_button["text"] = "Floor 4: OFF"

	def changeFloor3State(self):
		self.floor3_on = not self.floor3_on

		if self.floor3_on: # LEDs are now on
			floor3_led.on()
			self.floor3_button["bg"] = "lightgreen"
			self.floor3_button["text"] = "Floor 3: ON"
		else: # LEDs are now off
			floor3_led.off()
			self.floor3_button["bg"] = "red"
			self.floor3_button["text"] = "Floor 3: OFF"

	def changeFloor2State(self):
		self.floor2_on = not self.floor2_on

		if self.floor2_on: # LEDs are now on
			floor2_led.on()
			self.floor2_button["bg"] = "lightgreen"
			self.floor2_button["text"] = "Floor 2: ON"
		else: # LEDs are now off
			floor2_led.off()
			self.floor2_button["bg"] = "red"
			self.floor2_button["text"] = "Floor 2: OFF"

	def changeFloor1State(self):
		self.floor1_on = not self.floor1_on

		if self.floor1_on: # LEDs are now on
			floor1_led.on()
			self.floor1_button["bg"] = "lightgreen"
			self.floor1_button["text"] = "Floor 1: ON"
		else: # LEDs are now off
			floor1_led.off()
			self.floor1_button["bg"] = "red"
			self.floor1_button["text"] = "Floor 1: OFF"

