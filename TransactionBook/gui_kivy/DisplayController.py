from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from TransactionBook.model.TransactionBook import TransactionBook
from TransactionBook.gui_kivy.MainView import MainView
from TransactionBook.gui_kivy.TransactionViews import TransactionDetailsPopUp
from TransactionBook.model.Filter import Filter


class DisplayController(FloatLayout):
    def __init__(self, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        self.model = TransactionBook()

        self.TRANSACTIONS = "Transaction"
        self.EVALUATION = "Plots"
        self.NUMBERS = "Numbers"
        self.states = [self.TRANSACTIONS, self.NUMBERS, self.EVALUATION]
        self.state = self.states[0]

        # Filter
        self.transaction_filter = Filter()

        # Views
        self.main_view = MainView(ctrl=self)
        self.popup = None
        self.popup_size = (1000, 450)
        self.new_view = None

        #
        self.update()

    def update(self):
        if self.popup:
            self.popup.dismiss()
        self.clear_widgets()
        self.add_widget(self.main_view)
        self.main_view.update()

    def new_item(self):
        self.popup = TransactionDetailsPopUp(ctrl=self)

    def to_main_page(self):
        pass

    def on_size(self, *args):
        self.update()
        self.x, self.y = Window.size

    def on_stop(self):
        pass

    def on_start(self):
        pass

