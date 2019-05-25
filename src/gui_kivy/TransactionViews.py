from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout

from src.gui_kivy.generic.DropDownButton import DropDownButton
from src.gui_kivy.generic.datepicker import DatePicker
from src.gui_kivy.generic.ListPicker import ListPicker

class TransactionList(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.spacing = 10
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            self.add_widget(btn)


class TransactionDetails(AnchorLayout):
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

        # Input data
        self.grid.label_date = Label(text="Date:")
        self.grid.input_date = DatePicker()
        self.grid.label_acc_from = Label(text="Account from:")
        self.grid.input_acc_from = DropDownButton(ctrl.model.accounts, callback=None)
        self.grid.label_acc_to = Label(text="Account to")
        self.grid.input_acc_to = DropDownButton(ctrl.model.accounts, callback=None)
        self.grid.label_amount = Label(text="Amount:")
        self.grid.input_amount = TextInput(text="", multiline=False)
        self.grid.label_category = Label(text="Category:")
        self.grid.input_category = ListPicker(self.ctrl.model.categories,
                                              add_callback=self.cb_add_category,
                                              topic="Category")

        self.grid.label_description = Label(text="Description:")
        self.grid.input_description = TextInput(text="", multiline=False)

        # Buttons:
        self.grid.button_cancel = Button(text="Cancel")
        self.grid.button_cancel.bind(on_press=self.cancel_callback)
        self.grid.button_save = Button(text="Save")
        self.grid.button_save.bind(on_press=self.save_callback)

        self.add_widget(self.grid)
        self.update()

    def cb_add_category(self, text):
        # Write category text in text box
        self.grid.input_category.text = text
        # Add category to model
        self.ctrl.model.categories.append(text)
        # Update GUI element to take new category into account
        self.grid.input_category = ListPicker(self.ctrl.model.categories,
                                              add_callback=self.cb_add_category,
                                              topic="Category")
        self.update()

    def update(self):
        self.grid.clear_widgets()
        self.grid.add_widget(self.grid.label_date)
        self.grid.add_widget(self.grid.input_date)
        self.grid.add_widget(self.grid.label_acc_from)
        self.grid.add_widget(self.grid.input_acc_from)
        self.grid.add_widget(self.grid.label_acc_to)
        self.grid.add_widget(self.grid.input_acc_to)
        self.grid.add_widget(self.grid.label_amount)
        self.grid.add_widget(self.grid.input_amount)
        self.grid.add_widget(self.grid.label_category)
        self.grid.add_widget(self.grid.input_category)
        self.grid.add_widget(self.grid.label_description)
        self.grid.add_widget(self.grid.input_description)

        # Buttons:
        self.grid.add_widget(self.grid.button_cancel)
        self.grid.add_widget(self.grid.button_save)

    def cancel_callback(self, _):
        self.ctrl.update()

    def save_callback(self, _):
        self.ctrl.push_new_account(self.grid.input_name.text,
                                   self.grid.input_balance.text,
                                   self.grid.input_currency.text,
                                   self.grid.input_interest.text)
        self.ctrl.update()



