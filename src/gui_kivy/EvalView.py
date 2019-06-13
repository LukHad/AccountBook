from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import matplotlib.pyplot as plt


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
        self.add_widget(self.year_trend_box())
        self.add_widget(self.year_trend_box())
        self.add_widget(self.year_trend_box())

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

    def year_trend_box(self):
        plt.plot([1, 23, 2, 4])
        plt.ylabel('some numbers')
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box
