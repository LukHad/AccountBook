from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


class Menu(BoxLayout):
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

        self.selection_list = [self.SAVE, self.LOAD]  # Item list
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
            # self.save()
            print("Save")
        elif btn_text == self.LOAD:
            print("Load")

    def save(self):
        popup = ChooseFile()
        popup.open()


class ChooseFile(Popup):
    pHint_x = NumericProperty(0.7)
    pHint_y = NumericProperty(0.7)
    pHint = ReferenceListProperty(pHint_x, pHint_y)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_layout = BoxLayout(orientation="vertical")
        self.button_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        self.cancle = Button(text="Cancel")
        self.select = Button(text="OK")

        self.label_path = Label(text="Enter full path to data file")
        self.input_path = TextInput(text="")

        self.box_layout.add_widget(self.label_path)
        self.box_layout.add_widget(self.input_path)
        self.button_box.add_widget(self.cancle)
        self.button_box.add_widget(self.select)

        self.box_layout.add_widget(self.button_box)

        self.content = self.box_layout
        self.title = "Choose file"

        self.size_hint = self.pHint
        Window.release_all_keyboards()
        self.open()






