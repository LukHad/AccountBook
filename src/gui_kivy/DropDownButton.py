from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class DropDownButton(BoxLayout):
    """
    This class represents a "simple" drop down menu.
    """
    def __init__(self, selection_list, callback, **kwargs):
        """
        :param selection_list: list of strings with possible selections
        :param callback: callback to execute when a item is selected
        :param kwargs: optional BoxLayout arguments

        Selected string can be requested from .selection.
        """
        super().__init__(**kwargs)

        self.selection_list = selection_list  # Item list
        self.selection = selection_list[0]  # Currently selected item
        self.drop_down_button = Button(text=self.selection)
        self.drop_down_button.bind(on_release=lambda _: self.show_drop_down(callback))
        self.add_widget(self.drop_down_button)

    def show_drop_down(self, callback):
        def cb_item(btn):
            dp.select(btn.text)
            self.selection = btn.text
            callback()

        button = self.drop_down_button
        dp = DropDown()
        dp.bind(on_select=lambda instance, x: setattr(button, 'text', x))
        for txt in self.selection_list:
            item = Button(text=txt, size_hint_y=None, height=60)
            item.bind(on_release=lambda btn: cb_item(btn))
            dp.add_widget(item)
        dp.open(button)
