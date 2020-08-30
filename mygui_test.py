import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class newApp(App):
	def build(self):
		b = BoxLayout()
		button_1 = Button(text="Hello", font_size=20, size_hint=(None, None), width = 200, height = 50)
		b.add_widget(Label(text="Hello", font_size=20, size_hint=(None, None), width = 200, height = 50))
		b.add_widget(button_1)
		button_1.bind(on_hover=self.no)
		button_1.bind(on_press=self.ahh)

		return b

	def no(self, instance):
		print("Nooo")

	def ahh(self, instance):
		print("Yess more moree")
if __name__ == "__main__":
	myapp = newApp()
	myapp.run()