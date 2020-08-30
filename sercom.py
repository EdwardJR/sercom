import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from platform import system
import os
import serial
from time import sleep


kivy.require("1.11.1")


class ConnectPage(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 2


		if os.path.isfile('prev_details.txt'):
			with open('prev_details.txt', 'r') as f:
				d = f.read().split(',')

				prev_baudrate = d[0]
				prev_port = d[1]
				prev_parity = d[2]
				prev_data_bits = d[3]
				# prev_motor = d[4]
				# prev_direction = d[5]
				# prev_steps = d[6]

		else:

			prev_baudrate = ""
			prev_port = ""
			prev_parity = ""
			prev_data_bits = ""
			# prev_motor = ""
			# prev_direction = ""
			# prev_steps = ""


		self.add_widget(Label(text="Baudrate : "))
		self.baudrate = TextInput(text=prev_baudrate, multiline=False)
		self.add_widget(self.baudrate)


		self.add_widget(Label(text="Port : "))
		self.port = TextInput(text=prev_port, multiline=False)
		self.add_widget(self.port)


		self.add_widget(Label(text="Data bits : "))
		self.data_bits = TextInput(text=prev_data_bits, multiline=False)
		self.add_widget(self.data_bits)


		self.add_widget(Label(text="Parity : "))
		self.parity = TextInput(text=prev_parity, multiline=False)
		self.add_widget(self.parity)


		self.connect = Button(text="Connect")
		self.connect.bind(on_press=self.connect_button)
		self.add_widget(Label())
		self.add_widget(self.connect)


		self.add_widget(Label(text="motor : "))
		self.motor = TextInput(multiline=False)
		self.add_widget(self.motor)


		self.add_widget(Label(text="Direction : "))
		self.direction = TextInput(multiline=False)
		self.add_widget(self.direction)


		self.add_widget(Label(text="Steps : "))
		self.steps = TextInput(multiline=False)
		self.add_widget(self.steps)

		self.send_button = Button(text="Send")
		self.send_button.bind(on_press=self.send)
		self.add_widget(Label(text="SERCOM"))
		self.add_widget(self.send_button)


	def send(self, instance):
		steps 		= self.steps.text
		direction 	= self.direction.text
		motor 		= self.motor.text

		port 		= self.port.text
		baudrate 	= self.baudrate.text
		parity 		= self.parity.text
		data_bits 	= self.data_bits.text

		try:
			ser = serial.Serial(port, int(baudrate), int(data_bits), parity = 'N')
			ser.close()
			ser.open()
			ser.write(chr(int(motor)).encode())
			print(f"Selecting motor {motor}")
			sleep(1)
			ser.write(chr(int(direction)).encode())
			print(f"Selecting motor direction {direction}")
			sleep(1)
			ser.write(chr(int(steps)).encode())
			print(f"Number of steps {steps}")
			print(chr(int(steps)))
			print(chr(int(steps)).encode())
		except serial.SerialException:
			info = f"Device is disconneceted!"
			sercom_app.driver_page.update_info(info)
			sercom_app.screen_manager.current = "Driver"
			Clock.schedule_once(self.command_mode, 1)



	def connect_button(self, instance):
		port = self.port.text
		baudrate = self.baudrate.text
		parity = self.parity.text
		data_bits = self.data_bits.text

		with open('prev_details.txt', 'w') as f:
			f.write(f'{baudrate},{port},{parity},{data_bits}')

		if system() == "Linux":
			port = f"/dev/{port}"

		try:
			ser = serial.Serial(port, int(baudrate), int(data_bits), parity = 'N')
			ser.close()
			ser.open()
			
			if ser.is_open:
				info = f"Connected to {port} with a baudrate of {baudrate}"
			else:
				info = f"Connnection Failed!"
		except serial.SerialException:
			info = f"USB Device is not plugged in or refuses to connect!"

		sercom_app.driver_page.update_info(info)
		sercom_app.screen_manager.current = "Driver"
		Clock.schedule_once(self.command_mode, 1)

	def command_mode(self, _):
		sercom_app.screen_manager.current = "Connect"



class DriverPage(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 1

		self.message = Label(halign = "center", valign = "middle", font_size = 30)
		self.message.bind(width=self.update_text_width)
		self.add_widget(self.message)

	def update_info(self, message):
		self.message.text = message

	def update_text_width(self, *_):
		self.message.text_size = (self.message.width*0.9, None)


class Sercom(App):
	def build(self):

		self.screen_manager = ScreenManager()

		self.connect_page = ConnectPage()
		screen = Screen(name="Connect")
		screen.add_widget(self.connect_page)
		self.screen_manager.add_widget(screen)

		self.driver_page = DriverPage()
		screen = Screen(name="Driver")
		screen.add_widget(self.driver_page)
		self.screen_manager.add_widget(screen)


		return self.screen_manager

if __name__ == "__main__":
	sercom_app = Sercom()
	sercom_app.run()
