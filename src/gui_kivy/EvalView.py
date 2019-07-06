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
        self.filter_initialized = False

    def update(self):
        # Clear all widgets
        plt.close("all")
        self.clear_widgets()

        # Init filters
        if not self.filter_initialized:
            model = self.ctrl.model
            years = model.years()
            # Select most recent year as default
            self.filter_pie.select_date_range(model.DATE,
                                              datetime(max(years), 1, 1),
                                              datetime(max(years), 12, 31))
            self.filter_monthly_trend.select_date_range(model.DATE,
                                                        datetime(max(years), 1, 1),
                                                        datetime(max(years), 12, 31))
            # Select all categories
            for cat in model.categories:
                self.filter_pie.select(model.CATEGORY, cat)
                self.filter_monthly_trend.select(model.CATEGORY, cat)
            # Select all categories
            for acc in model.accounts:
                self.filter_pie.select(model.ACCOUNT, acc)
                self.filter_monthly_trend.select(model.ACCOUNT, acc)

            self.filter_initialized = True
        # End Init filters

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
        fig = plt.figure()
        button_grid = self.get_filter_grid(self.filter_monthly_trend, year_multiselect=False)
        box = BoxLayout()
        box.add_widget(button_grid)
        box.orientation = 'vertical'

        # Get data
        df_filtered = self.filter_monthly_trend.filter(self.ctrl.model.data)
        if not df_filtered.empty:
            label, data = self.ctrl.model.pivot_monthly_trend(df_filtered)  # ToDo: Implement year selection / dropdown
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
            box.add_widget(FigureCanvasKivyAgg(fig))
        else:
            no_data_label = Label(text="Not enough data")
            box.add_widget(no_data_label)
        return box

    def category_expenses_pie_box(self):
        # Clear old figure
        # Get data
        df = self.ctrl.model.data
        df_filtered = self.filter_pie.filter(df)
        button_grid = self.get_filter_grid(self.filter_pie)
        box = BoxLayout()
        box.add_widget(button_grid)
        box.orientation = 'vertical'
        if not df_filtered.empty:
            label, data = self.ctrl.model.pivot_category_pie(df_filtered, percent=True)  # ToDo: Implement year selection / dropdown
            # Create plot item
            fig, ax = plt.subplots()
            wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%')
            ax.axis('equal')  # Equal aspect ratio esures that pie is drawn as a circle.
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

    def get_filter_grid(self, my_filter, year_multiselect=True):
        button_grid = GridLayout(rows=1, size_hint=(1, 0.075))
        button_date = Button(text=self.ctrl.model.DATE)
        button_date.bind(on_release=lambda l_f: self.set_filter(my_filter, button_date.text, year_multiselect))
        button_acc = Button(text=self.ctrl.model.ACCOUNT)
        button_acc.bind(on_release=lambda l_f: self.set_filter(my_filter, button_acc.text))
        button_cat = Button(text=self.ctrl.model.CATEGORY)
        button_cat.bind(on_release=lambda l_f: self.set_filter(my_filter, button_cat.text))
        button_grid.add_widget(button_date)
        button_grid.add_widget(button_acc)
        button_grid.add_widget(button_cat)
        return button_grid

    def set_filter(self, my_filter, topic, year_multiselect=True):
        model = self.ctrl.model

        def cb(new_selected_list):
            my_filter.filter_select[topic] = new_selected_list
            self.update()

        def cb_date(year_str_list):
            year = list(map(int, year_str_list))
            from_date = datetime(min(year), 1, 1)
            to_date = datetime(max(year), 12, 31)
            my_filter.select_date_range(topic, from_date, to_date)
            self.update()

        f = my_filter
        if topic == model.CATEGORY:
            options = model.categories
            callback = cb
            selection = f.check_if_selected(topic, options)
            MultiSelectPopUp(title=topic, option_list=options, option_init=selection, callback=callback)
        elif topic == model.ACCOUNT:
            options = model.accounts
            callback = cb
            selection = f.check_if_selected(topic, options)
            MultiSelectPopUp(title=topic, option_list=options, option_init=selection, callback=callback)
        else:
            options = model.years()
            callback = cb_date
            date_range = f.filter_date_time[topic]
            selection = []
            for opt in options:
                if (int(opt) >= date_range[0].year) and (int(opt) <= date_range[1].year):
                    selection.append(True)
                else:
                    selection.append(False)
            MultiSelectPopUp(title=topic, option_list=options, option_init=selection, callback=callback,
                             multiselect=year_multiselect)
