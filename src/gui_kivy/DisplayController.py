from kivy.uix.floatlayout import FloatLayout
# Internal imports
from src.Adapter import Adapter
from src.gui_kivy.Topbar import Topbar
from src.gui_kivy.Sidebar import Sidebar
from src.gui_kivy.Details import Details
from src.gui_kivy.AccountDetails import AccountDetails

# Dimensions
SIDEBAR_WIDTH = 0.1
TOPBAR_WIDTH = 0.05


class DisplayController(FloatLayout):
    """
    Main Class of GUI, Layout:
          Topbar
    -----------------
    Sidebar | Details
    """
    def __init__(self, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        self.states = ["Accounts", "Evaluation", "Categories", "Standing orders"]
        # Create widgets
        self.topbar = Topbar(pos_hint={'y': 1-TOPBAR_WIDTH}, size_hint=(1, TOPBAR_WIDTH), ctrl=self)
        self.sidebar = Sidebar(pos=(0, 0), size_hint=(SIDEBAR_WIDTH, 1-TOPBAR_WIDTH))
        self.details = Details(pos_hint={'x': SIDEBAR_WIDTH}, size_hint=(1-SIDEBAR_WIDTH, 1-TOPBAR_WIDTH))
        self.acc_details = AccountDetails()
        # Add widgets to Display
        self.add_widget(self.topbar)
        self.add_widget(self.sidebar)
        self.add_widget(self.details)
        #
        self.active_state = self.states[0]
        self.update()

    def update(self):
        # Update top bar
        button_list = []
        if self.active_state == self.states[0]:
            # Update sidebar
            button_list = Adapter().req_acc_list()
            # Update details content
            self.details.update(content=self.acc_details)
        elif self.active_state == "Categories":
            button_list = Adapter().req_cat_list()
        else:
            print("Dummy: View not implemented")
            pass
        self.sidebar.update(button_list)

    def on_size(self, *args):
        """
        Resize callback
        """
        self.update()
