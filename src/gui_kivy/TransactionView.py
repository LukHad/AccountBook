from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout


class TransactionNew(AnchorLayout):
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.anchor_y = 'top'
        self.ctrl = ctrl

        self.grid = GridLayout()
        self.grid.cols = 2
        self.grid.spacing = 10
        self.grid.size_hint_y = None
        self.grid.bind(minimum_height=self.setter('height'))
        self.grid.row_default_height = 40

        self.grid.label_name = Label(text="Account name:")
        self.grid.input_name = TextInput(text=" ", multiline=False)
        self.grid.label_balance = Label(text="Account balance:")
        self.grid.input_balance = TextInput(text="0.0", multiline=False)
        self.grid.label_currency = Label(text="Currency:")
        self.grid.input_currency = TextInput(text="Euro", multiline=False)
        self.grid.label_interest = Label(text="Interest in %")
        self.grid.input_interest = TextInput(text="0.0", multiline=False)

        self.grid.button_cancel = Button(text="Cancel")
        self.grid.button_cancel.bind(on_press=self.cancel_callback)
        self.grid.button_save = Button(text="Save")
        self.grid.button_save.bind(on_press=self.save_callback)

        self.update()

    def update(self):
        self.grid.clear_widgets()
        self.grid.add_widget(self.grid.label_name)
        self.grid.add_widget(self.grid.input_name)
        self.grid.add_widget(self.grid.label_balance)
        self.grid.add_widget(self.grid.input_balance)
        self.grid.add_widget(self.grid.label_currency)
        self.grid.add_widget(self.grid.input_currency)
        self.grid.add_widget(self.grid.label_interest)
        self.grid.add_widget(self.grid.input_interest)
        self.grid.add_widget(self.grid.button_cancel)
        self.grid.add_widget(self.grid.button_save)
        self.add_widget(self.grid)

    def cancel_callback(self, _):
        self.ctrl.to_main_page()

    def save_callback(self, _):
        self.ctrl.push_new_account(self.grid.input_name.text,
                                   self.grid.input_balance.text,
                                   self.grid.input_currency.text,
                                   self.grid.input_interest.text)


class TransactionDetails(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.spacing = 10
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            self.add_widget(btn)
