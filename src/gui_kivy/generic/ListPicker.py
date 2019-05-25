from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from src.gui_kivy.generic.InputBox import InputBox


class ListPicker(TextInput):
    pHint_x = NumericProperty(0.7)
    pHint_y = NumericProperty(0.7)
    pHint = ReferenceListProperty(pHint_x, pHint_y)

    def __init__(self, element_list, add_callback=None, topic="Select item", **kwargs):
        super().__init__()
        self.text = ""
        self.topic = topic
        self.element_list = element_list
        self.add_callback = add_callback

        self.scroll_view = ScrollView()
        self.grid = GridLayout(cols=1)
        self.scroll_view.add_widget(self.grid)
        for el in element_list:
            btn_act = Button(text=el)
            btn_act.bind(on_release=lambda btn: self.cb_item(btn))
            self.grid.add_widget(btn_act)

        if add_callback:
            add_button = Button(text="+ Add new")
            add_button.bind(on_release=lambda btn: self.cb_add_new())
            self.grid.add_widget(add_button)

        self.popup = Popup(title=f"Select {topic}", content=self.scroll_view)

        self.bind(focus=self.show_popup)

    def show_popup(self, isnt, val):
        """
        Open popup if textinput focused,
        and regardless update the popup size_hint
        """
        self.popup.size_hint=self.pHint
        if val:
            # Automatically dismiss the keyboard
            # that results from the textInput
            Window.release_all_keyboards()
            self.popup.open()

    def cb_item(self, btn):
        self.text = btn.text
        self.popup.dismiss()

    def cb_add_new(self):
        InputBox(title=f"Add new {self.topic}", callback=self.add_callback)
        self.popup.dismiss()


if __name__ == "__main__":
    from kivy.base import runTouchApp
    c = ListPicker(["Item1", "Item2", "Item3"])
    runTouchApp(c)