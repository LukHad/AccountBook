from kivy.uix.floatlayout import FloatLayout
from src.gui_kivy.Topbar import Topbar
from src.gui_kivy.Sidebar import Sidebar
from src.gui_kivy.Details import Details


class MainView(FloatLayout):
    """
    Main Class of GUI, Layout:
          Topbar
    -----------------
    Sidebar | Details
    """
    def __init__(self, ctrl, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        # Create widgets
        sidebar_width = 0.1
        top_bar_width = 0.05
        self.topbar = Topbar(pos_hint={'y': 1-top_bar_width}, size_hint=(1, top_bar_width), ctrl=ctrl)
        self.sidebar = Sidebar(pos=(0, 0), size_hint=(sidebar_width, 1-top_bar_width))
        self.details = Details(pos_hint={'x': sidebar_width}, size_hint=(1-sidebar_width, 1-top_bar_width))
        self.update()

    def update(self):
        self.clear_widgets()
        # Add widgets to Display
        self.add_widget(self.topbar)
        self.add_widget(self.sidebar)
        self.add_widget(self.details)
        self.details.update()
        self.sidebar.update()


