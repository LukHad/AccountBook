from kivy.uix.floatlayout import FloatLayout
# Internal imports
from src.Adapter import Adapter
from src.gui_kivy.MainView import MainView
from src.gui_kivy.AccountView import AccountNew

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
        self.page = MAIN_PAGE
        self.states = [ACCOUNTS, EVALUATION, CATEGORIES, STANDINGS]
        self.active_state = self.states[0]
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
                button_list = Adapter().req_acc_list()
                self.main_view.details.content = self.main_view.details.account_details
            elif self.active_state == CATEGORIES:
                button_list = Adapter().req_cat_list()
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
            print("New callback triggered")
            self.new_view = AccountNew(ctrl=self)
            self.page = NEW_PAGE
        self.update()

    def to_main_page(self):
        self.page = MAIN_PAGE
        self.update()

    def on_size(self, *args):
        self.update()
