from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import matplotlib.pyplot as plt
import matplotlib
import datetime
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.checkbox import CheckBox
from TransactionBook.gui_kivy.generic.MultiSelectPopUp import MultiSelectPopUp
import numpy as np


class NumbersView(GridLayout):
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.ctrl = ctrl
        # Layout:
        self.cols = 1
        self.spacing = 10
        self.size_hint_y = None
        self.height = 120  # ToDo: Check magic number on other displays
        self.bind(minimum_height=self.setter('height'))

    def update(self):
        self.clear_widgets()

        # Add widgets
        self.add_widget(self.account_balance_box())

    def account_balance_box(self):
        box = GridLayout()
        box.cols = 3

        m = self.ctrl.model
        total_balance = m.total_balance(m.get_data())

        # Heading:
        box.add_widget(Label(text="Name"))
        box.add_widget(Label(text="Balance"))
        box.add_widget(Label(text="% of total"))
        for acc in m.accounts:
            # Calculate account balance
            balance = m.account_balance(acc, m.get_data())
            balance_str = f"{balance:.2f} {m.CURRENCY}"
            percentage = (balance / total_balance)*100
            percentage_str = f"{percentage:.2f} %"

            acc_label = Label(text=acc)
            balance_label = Label(text=balance_str)
            percentage_label = Label(text=percentage_str)

            box.add_widget(acc_label)
            box.add_widget(balance_label)
            box.add_widget(percentage_label)
        return box

