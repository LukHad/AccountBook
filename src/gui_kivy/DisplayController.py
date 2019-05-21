from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import numbers
# Internal imports
from src.Adapter import Adapter
from src.gui_kivy.MainView import MainView
from src.gui_kivy.AccountView import AccountNew
from src.gui_kivy.MsgBox import MsgBox


ACCOUNTS = "Accounts"
EVALUATION = "Evaluation"
CATEGORIES = "Categories"
STANDINGS = "Standing orders"

MAIN_PAGE = 1
NEW_PAGE = 2


class DisplayController(FloatLayout):
    def __init__(self, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        self.x = 0
        self.y = 0
        self.page = MAIN_PAGE
        self.states = [ACCOUNTS, EVALUATION, CATEGORIES, STANDINGS]
        self.active_state = self.states[0]
        self.adapter = Adapter()
        # Views
        self.main_view = MainView(ctrl=self)
        self.new_view = None
        self.update()

    def update(self):
        self.clear_widgets()
        if self.page == MAIN_PAGE:
            self.add_widget(self.main_view)
            self.active_state = self.main_view.topbar.drop_down_button.selection
            if self.active_state == ACCOUNTS:
                # Update sidebar
                button_list = self.adapter.req_acc_list()
                self.main_view.details.content = self.main_view.details.account_details
            elif self.active_state == CATEGORIES:
                button_list = self.adapter.req_cat_list()
                self.main_view.details.content = None
            else:
                button_list = []
                print("Dummy: View not implemented")
                pass
            self.main_view.sidebar.button_str_list = button_list
            self.main_view.update()
        elif self.page == NEW_PAGE:
            self.add_widget(self.new_view)

    def new_item(self):
        if self.active_state == ACCOUNTS:
            self.new_view = AccountNew(ctrl=self)
            self.page = NEW_PAGE
        self.update()

    def to_main_page(self):
        self.page = MAIN_PAGE
        self.update()

    def on_size(self, *args):
        self.update()
        self.x, self.y = Window.size

    def on_stop(self):
        self.adapter.save()

    def on_start(self):
        self.adapter.load()

    def push_new_account(self, name, balance, currency, interest):
        if len(name) < 2:
            MsgBox("Account name must be more than 2 digits")
            return
        if balance.isnumeric():
            balance = float(balance)
        else:
            MsgBox("Balance must be a numeric value")
            return
        if interest.isnumeric():
            interest = float(interest) / 100.0
        else:
            MsgBox("Interest must be a numeric value")
            return
        self.adapter.push_new_account(name, balance, currency, interest)
        self.page = MAIN_PAGE
        self.update()

