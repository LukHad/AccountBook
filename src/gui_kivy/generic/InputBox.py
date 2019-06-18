from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class InputBox:
    def __init__(self, callback, title="", text="", size=(600, 250)):
        self.callback = callback
        self.grid = GridLayout(cols=1)
        self.grid.size_hint_y = None
        self.grid.row_default_height = 50
        self.grid.spacing = 10

        self.grid.input_text = TextInput(text=text)
        self.grid.ok = Button(text="OK")
        self.grid.add_widget(self.grid.input_text)
        self.grid.add_widget(self.grid.ok)

        self.popup = Popup(title=title, content=self.grid, size=size, size_hint=(None, None))
        self.grid.ok.bind(on_release=lambda _: self.cb_ok())

        self.popup.open()

    def cb_ok(self):
        self.text = self.grid.input_text.text
        self.callback(self.text)
        self.popup.dismiss()

