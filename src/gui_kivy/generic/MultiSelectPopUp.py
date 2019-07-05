from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import matplotlib.pyplot as plt
import matplotlib
import datetime
from src.model.Filter import Filter
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window


class MultiSelectPopUp(Popup):
    pHint_x = NumericProperty(0.7)
    pHint_y = NumericProperty(0.7)
    pHint = ReferenceListProperty(pHint_x, pHint_y)

    def __init__(self, title, option_list, option_init=None, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.callback = callback
        self.main_layout = AnchorLayout()
        if option_init is None:
            option_init = [True] * len(option_list)

        self.grid = GridLayout(cols=2)
        self.opt_boxes = []
        self.labels = []
        for i, opt in enumerate(option_list):
            check_box = CheckBox(active=option_init[i])
            label = Label(text=opt)
            self.opt_boxes.append(check_box)
            self.labels.append(label)
            self.grid.add_widget(check_box)
            self.grid.add_widget(label)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.cancel_callback)
        ok_button = Button(text="Ok")
        ok_button.bind(on_press=self.ok_callback)
        self.grid.add_widget(cancel_button)
        self.grid.add_widget(ok_button)

        self.main_layout.add_widget(self.grid)

        self.content = self.main_layout
        self.size_hint = self.pHint
        Window.release_all_keyboards()
        self.open()

    def ok_callback(self, _):
        selection = []
        for i, check_box in enumerate(self.opt_boxes):
            if check_box.active:
                selection.append(self.labels[i].text)
        self.callback(selection)
        self.dismiss()

    def cancel_callback(self, _):
        self.dismiss()


if __name__ == "__main__":
    from kivy.base import runTouchApp

    def cb(list_of_selection):
        print(list_of_selection)
    c = MultiSelectPopUp(title="Test", option_list=["Item1", "Item2", "Item3"], callback=cb, option_init=[True, False, True])
    runTouchApp(c)