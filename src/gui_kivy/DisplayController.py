from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from src.model.TransactionBook import TransactionBook
from src.gui_kivy.MainView import MainView
from src.gui_kivy.TransactionViews import TransactionDetails


class DisplayController(FloatLayout):
    def __init__(self, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        self.model = TransactionBook()

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
        if self.state == self.TRANSACTIONS:
            self.clear_widgets()
            self.add_widget(TransactionDetails(ctrl=self))


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

