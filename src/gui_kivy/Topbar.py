from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class Topbar(BoxLayout):
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.ctrl = ctrl
        self.orientation = 'horizontal'

        self.drop_down_button = Button(text=ctrl.states[0])
        self.drop_down_button.bind(on_release=lambda _: self.show_dropdown())

        self.button_new = Button(text="new")

        self.add_widget(self.drop_down_button)
        self.add_widget(self.button_new)

    def show_dropdown(self):
        def cb_item(btn):
            dp.select(btn.text)
            self.ctrl.active_state = btn.text
            self.ctrl.update()

        button = self.drop_down_button
        dp = DropDown()
        dp.bind(on_select=lambda instance, x: setattr(button, 'text', x))
        for txt in self.ctrl.states:
            item = Button(text=txt, size_hint_y=None, height=60)
            # item.bind(on_release=lambda btn: dp.select(btn.text))
            item.bind(on_release=lambda btn: cb_item(btn))
            dp.add_widget(item)
        dp.open(button)





