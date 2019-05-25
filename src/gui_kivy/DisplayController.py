from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import numbers
# Internal imports
from src.model.TransactionBook import TransactionBook
from src.gui_kivy.MainView import MainView
from src.gui_kivy.TransactionView import TransactionNew
from src.gui_kivy.MsgBox import MsgBox


class DisplayController(FloatLayout):
    def __init__(self, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        self.x = 0
        self.y = 0

        self.TRANSACTIONS = "Transaction"
        self.EVALUATION = "Evaluation"
        self.states = [self.TRANSACTIONS, self.EVALUATION]
        self.state = self.states[0]

        # Views
        self.main_view = MainView(ctrl=self)
        self.new_view = None
        self.update()

    def update(self):
        self.clear_widgets()
        self.add_widget(self.main_view)
        self.main_view.update()

    def new_item(self):
        pass

    def to_main_page(self):
        pass

    def on_size(self, *args):
        self.update()
        self.x, self.y = Window.size

    def on_stop(self):
        pass

    def on_start(self):
        pass

    def push_new_account(self, name, balance, currency, interest):
        pass

