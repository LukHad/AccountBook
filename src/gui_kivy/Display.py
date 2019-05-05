from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
# Internal imports
from src.Adapter import Adapter
from src.gui_kivy.Sidebar import Sidebar
from src.gui_kivy.Details import Details
from src.gui_kivy.AccountDetails import AccountDetails

class Display(FloatLayout):
    """
    Main Class of GUI
    Sidebar | Details
    """
    # Dimensions
    SIDEBAR_WIDTH = 0.1
    # States
    ACCOUNT_VIEW = 0
    ANALYSIS_VIEW = 1
    # Labels
    ACCOUNT_VIEW_LABEL = "Account view"
    ANALYSIS_VIEW_LABEL = "Analysis view"

    def __init__(self, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        # Create widgets
        self.sidebar = Sidebar(pos=(0, 0), size_hint=(Display.SIDEBAR_WIDTH, 1))
        self.details = Details(pos_hint={'x': Display.SIDEBAR_WIDTH}, size_hint=(1-Display.SIDEBAR_WIDTH, 1))
        # Add widgets to Display
        self.add_widget(self.sidebar)
        self.add_widget(self.details)
        #
        self.active_view = Display.ACCOUNT_VIEW
        self.update_current_view()

    def update_current_view(self):
        if self.active_view == Display.ACCOUNT_VIEW:
            # Update sidebar
            button_list = Adapter().req_acc_list()
            self.sidebar.update(button_list)
            # Update details content
            self.details.update(content=AccountDetails())
        elif self.active_view == Display.ANALYSIS_VIEW:
            pass

    def on_size(self, *args):
        """
        Resize callback
        """
        self.update_current_view()
