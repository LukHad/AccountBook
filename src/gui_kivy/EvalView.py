from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
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
        self.add_widget(self.category_expenses_pie_box())

    def account_balance_box(self):
        box = GridLayout()
        box.cols = 2

        m = self.ctrl.model
        for acc in m.accounts:
            # Calculate account balance
            balance = m.account_balance(acc, m.data)
            balance_str = f"{balance:.2f} {m.CURRENCY}"

            acc_label = Label(text=acc)
            balance_label = Label(text=balance_str)

            box.add_widget(acc_label)
            box.add_widget(balance_label)
        return box

    def monthly_trend_box(self):
        # Clear old figure
        fig = plt.figure()
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
        plt.xticks(rotation=25)
        # Add Grid
        plt.grid(True)
        # Package in layout
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(fig))
        return box

    def category_expenses_pie_box(self):
        # Clear old figure
        # Get data
        label, data = self.ctrl.model.pivot_category_pie(datetime.date.today().year, percent=True)  # ToDo: Implement year selection / dropdown
        # Create plot item
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.legend(wedges, label,
                  title=self.ctrl.model.CATEGORY,
                  loc="center left",
                  bbox_to_anchor=(0.6, 0, 0.5, 1))
        ax.set_xlim(right=3)
        box = BoxLayout()
        # Add filter button
        button = Button(text='Filter', size_hint=(1, 0.075))
        box.add_widget(button)
        box.orientation = 'vertical'
        # Add plot canvas
        box.add_widget(FigureCanvasKivyAgg(fig))
        return box
