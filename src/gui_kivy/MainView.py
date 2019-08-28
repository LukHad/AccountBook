from kivy.uix.floatlayout import FloatLayout
from src.gui_kivy.Topbar import Topbar
from kivy.uix.scrollview import ScrollView
from src.gui_kivy.TransactionViews import TransactionList
from kivy.core.window import Window
from src.gui_kivy.EvalView import EvalView
from src.gui_kivy.NumbersView import NumbersView

class MainView(FloatLayout):
    """
          Topbar
    -----------------
       full_details
    """
    def __init__(self, ctrl, **kwargs):
        # Init parent
        super().__init__(**kwargs)
        # Create widgets
        self.sidebar_width = 0.1
        self.top_bar_abs_height = 50
        self.ctrl = ctrl
        # Create GUI objects
        # topbar is always visible
        self.topbar = Topbar(ctrl=ctrl, size_hint_y=None, height=self.top_bar_abs_height, pos_hint={'top': 1})
        self.scroll_view = ScrollView()

        # Populate GUI objects
        self.transaction_details = TransactionList(ctrl=self.ctrl)
        self.eval_view = EvalView(ctrl=self.ctrl)
        self.num_view = NumbersView(ctrl=self.ctrl)

        self.update()

    def update(self):
        self.ctrl.state = self.topbar.drop_down_button.selection
        self.clear_widgets()
        self.scroll_view.clear_widgets()
        # Calculate dimensions:
        _, window_height = Window.size
        top_bar_width = 50.0 / window_height
        self.scroll_view.size_hint = (1, 1 - top_bar_width)
        self.add_widget(self.scroll_view)
        if self.ctrl.state == self.ctrl.TRANSACTIONS:
            self.scroll_view.add_widget(self.transaction_details)
            self.transaction_details.update()
        elif self.ctrl.state == self.ctrl.EVALUATION:
            self.scroll_view.add_widget(self.eval_view)
            self.eval_view.update()
        elif self.ctrl.state == self.ctrl.NUMBERS:
            self.scroll_view.add_widget(self.num_view)
            self.num_view.update()

        self.add_widget(self.topbar)




