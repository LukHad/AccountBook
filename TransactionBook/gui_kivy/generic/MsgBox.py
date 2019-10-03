from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class MsgBox:
    def __init__(self, msg, title="Warning"):
        self.grid = GridLayout(cols=1)
        self.grid.msg = Label(text=msg)
        self.grid.ok = Button(text="OK")
        self.grid.add_widget(self.grid.msg)
        self.grid.add_widget(self.grid.ok)

        self.popup = Popup(title=title, content=self.grid, size=(600, 400), size_hint=(None, None))
        self.grid.ok.bind(on_press=lambda *args: self.popup.dismiss())
        self.popup.open()

