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
from src.model.Filter import Filter
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.checkbox import CheckBox
from src.gui_kivy.generic.MultiSelectPopUp import MultiSelectPopUp
import numpy as np

font = {'weight': 'bold',
        'size': 12}

matplotlib.rc('font', **font)


class EvalView(GridLayout):
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.ctrl = ctrl
        self.cols = 2

        self.filter_pie = Filter()
        self.filter_monthly_trend = Filter()

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
        label, data = self.ctrl.model.pivot_monthly_trend(2019)  # ToDo: Implement year selection / dropdown
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
        df = self.ctrl.model.data
        df_filtered = self.filter_pie.filter(df)
        button_grid = GridLayout(rows=1, size_hint=(1, 0.075))
        button_date = Button(text=self.ctrl.model.DATE)
        button_acc = Button(text=self.ctrl.model.ACCOUNT)
        button_cat = Button(text=self.ctrl.model.CATEGORY)
        button_cat.bind(on_press=self.set_pie_category_filter)
        button_grid.add_widget(button_date)
        button_grid.add_widget(button_acc)
        button_grid.add_widget(button_cat)
        box = BoxLayout()
        box.add_widget(button_grid)
        box.orientation = 'vertical'
        if not df_filtered.empty:
            label, data = self.ctrl.model.pivot_category_pie(df_filtered, percent=True)  # ToDo: Implement year selection / dropdown
            # Create plot item
            fig, ax = plt.subplots()
            wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%')
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.legend(wedges, label,
                      title=self.ctrl.model.CATEGORY,
                      loc="center left",
                      bbox_to_anchor=(0.6, 0, 0.5, 1))
            ax.set_xlim(right=3)
            # Add plot canvas
            box.add_widget(FigureCanvasKivyAgg(fig))
        else:
            no_data_label = Label(text="Not enough data")
            box.add_widget(no_data_label)
        return box

    def set_pie_category_filter(self, _):
        model = self.ctrl.model

        def cb(new_selected_list):
            self.filter_pie.filter_select[model.CATEGORY] = new_selected_list
            self.update()
        f = self.filter_pie
        selection = f.check_if_selected(model.CATEGORY, model.categories)
        MultiSelectPopUp(title=model.CATEGORY, option_list=model.categories, option_init=selection, callback=cb)
