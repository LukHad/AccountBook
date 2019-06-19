from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import matplotlib.pyplot as plt
import matplotlib
import datetime
import numpy as np

font = {'weight': 'bold',
        'size': 12}

matplotlib.rc('font', **font)


class EvalView(GridLayout):
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.ctrl = ctrl

        self.cols = 2

    def update(self):
        # Clear all widgets
        self.clear_widgets()

        # Add widgets
        self.add_widget(self.account_balance_box())
        self.add_widget(self.monthly_trend_box())

    def account_balance_box(self):
        box = GridLayout()
        box.cols = 2

        m = self.ctrl.model
        for acc in m.accounts:
            # Calculate account balance
            balance = m.account_balance(acc, m.data)
            balance_str = f"{balance} {m.CURRENCY}"

            acc_label = Label(text=acc)
            balance_label = Label(text=balance_str)

            box.add_widget(acc_label)
            box.add_widget(balance_label)
        return box

    def monthly_trend_box(self):
        # Clear old figure
        plt.clf()
        # Get data
        label, data = self.ctrl.model.pivot_monthly_trend(datetime.date.today().year)  # ToDo: Implement year selection / dropdown
        # Plot data and switch color depending on sign of months balance
        for i, dat in enumerate(data):
            if dat >= 0:
                plt.bar(label[i], dat, color='blue')
            else:
                plt.bar(label[i], dat, color='red')
        # Add currency as y-Label
        plt.ylabel(self.ctrl.model.CURRENCY)
        # Set x-Label vertical
        plt.xticks(rotation='vertical')
        # Add Grid
        plt.grid(True)
        # Package in layout
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box
