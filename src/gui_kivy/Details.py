from kivy.uix.scrollview import ScrollView
from src.gui_kivy.AccountView import AccountDetails


class Details(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.account_details = AccountDetails()
        self.content = self.account_details
        self.update()

    def update(self):
        self.clear_widgets()
        if self.content:
            self.add_widget(self.content)

