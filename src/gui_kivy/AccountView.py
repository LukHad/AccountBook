from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class AccountNew(GridLayout):
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.ctrl = ctrl
        self.label_name = Label(text="Account name:")
        self.input_name = TextInput(text=" ", multiline=False)

        self.button_cancel = Button(text="Cancel")
        self.button_cancel.bind(on_press=self.cancel_callback)
        self.button_save = Button(text="Save")

        self.update()

    def update(self):
        self.add_widget(self.label_name)
        self.add_widget(self.input_name)
        self.add_widget(self.button_cancel)
        self.add_widget(self.button_save)

    def cancel_callback(self, _):
        self.ctrl.to_main_page()


class AccountDetails(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.spacing = 10
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            self.add_widget(btn)
