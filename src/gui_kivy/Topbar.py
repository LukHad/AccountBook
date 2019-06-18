from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from src.gui_kivy.generic.DropDownButton import DropDownButton
from src.gui_kivy.Menu import Menu


class Topbar(BoxLayout):
    """
    DropDown | New-Button
    """
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.ctrl = ctrl
        self.orientation = 'horizontal'

        # Add drop down menu for main GUI options
        self.menu = Menu(self.ctrl)
        self.add_widget(self.menu)

        self.drop_down_button = DropDownButton(ctrl.states, ctrl.update)
        self.add_widget(self.drop_down_button)

        # Add button for new item
        self.button_new = Button(text="new")
        self.button_new.bind(on_press=self.new_callback)
        self.add_widget(self.button_new)

    def new_callback(self, _):
        self.ctrl.new_item()







