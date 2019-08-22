from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from src.gui_kivy.generic.InputBox import InputBox
from kivy.core.window import Window

from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


class Menu(BoxLayout):
    DB_PATH = "Database path"
    SAVE = "Save"
    LOAD = "Load"

    def __init__(self, ctrl, **kwargs):
        """
        :param selection_list: list of strings with possible selections
        :param callback: callback to execute when a item is selected
        :param kwargs: optional BoxLayout arguments

        Selected string can be requested from .selection.
        """
        super().__init__(**kwargs)
        self.ctrl = ctrl

        self.selection_list = [self.DB_PATH, self.LOAD, self.SAVE]  # Item list
        self.drop_down_button = Button(text="Menu")
        self.drop_down_button.bind(on_release=lambda _: self.show_drop_down())
        self.add_widget(self.drop_down_button)

    def show_drop_down(self):
        def cb_item(btn):
            dp.select(btn.text)
            self.selection = btn.text
            self.callback(btn.text)

        button = self.drop_down_button
        dp = DropDown()
        for txt in self.selection_list:
            item = Button(text=txt, size_hint_y=None, height=60)
            item.bind(on_release=lambda btn: cb_item(btn))
            dp.add_widget(item)
        dp.open(button)

    def callback(self, btn_text):
        if btn_text == self.SAVE:
            self.save()
        elif btn_text == self.LOAD:
            self.load()
        elif btn_text == self.DB_PATH:
            self.db_path()

    def db_path(self):
        x, y = Window.size
        size = (x, 250)
        InputBox(title="Enter path to data base",
                 callback=self.config_path,
                 text=self.ctrl.model.path,
                 size=size)

    def config_path(self, path):
        self.ctrl.model.path = path

    def save(self):
        model = self.ctrl.model
        if model.path != "":
            # ToDo: Check for valid directory path
            model.save()
        else:
            self.db_path()

    def load(self):
        model = self.ctrl.model
        if model.path != "":
            # ToDo: Check for valid file path
            model.load()
        else:
            self.db_path()
        self.ctrl.update()




