from kivy.uix.floatlayout import FloatLayout
from src.gui_kivy.Topbar import Topbar
from src.gui_kivy.generic.Sidebar import Sidebar
from kivy.uix.scrollview import ScrollView
from src.gui_kivy.TransactionViews import TransactionList


class MainView(FloatLayout):
    def __init__(self, ctrl, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        # Create widgets
        self.sidebar_width = 0.1
        self.top_bar_width = 0.05
        self.ctrl = ctrl
        # Create GUI objects
        # topbar is always visible
        self.topbar = Topbar(pos_hint={'y': 1 - self.top_bar_width}, size_hint=(1, self.top_bar_width), ctrl=ctrl)
        # sidebar and split_details always visible together
        self.sidebar = Sidebar(pos=(0, 0), size_hint=(self.sidebar_width, 1 - self.top_bar_width))
        self.split_details = ScrollView(pos_hint={'x': self.sidebar_width},
                                        size_hint=(1 - self.sidebar_width, 1 - self.top_bar_width))
        # full_details takes the entire space of sidebar and split_details
        self.full_details = ScrollView(size_hint=(1, 1 - self.top_bar_width))

        # Populate GUI objects
        self.transaction_details = TransactionList()
        self.full_details.add_widget(self.transaction_details)
        self.evaluation_details = TransactionList()  # temporary as a dummy
        self.split_details.add_widget(self.evaluation_details )
        self.sidebar.button_str_list = ["Year overview", "Custom graphs"]  # temporary as a dummy -> delete

        self.update()

    def update(self):
        self.ctrl.state = self.topbar.drop_down_button.selection
        self.clear_widgets()
        if self.ctrl.state == self.ctrl.TRANSACTIONS:
            """
                    Topbar
            -----------------------
            Sidebar | split_details
            """
            self.add_widget(self.full_details)
        elif self.ctrl.state == self.ctrl.EVALUATION:
            """
                  Topbar
            -----------------
               full_details
            """
            self.add_widget(self.split_details)
            self.add_widget(self.sidebar)
            self.sidebar.update()

        self.add_widget(self.topbar)




