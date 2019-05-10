from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class Sidebar(BoxLayout):
    def __init__(self, button_str_list=[], **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.button_str_list = button_str_list
        self.btn_list = []

    def update(self):
        # Clear button list
        self.clear_widgets()
        self.btn_list = []
        # Add new buttons
        for txt in self.button_str_list:
            new_button = Button(text=txt)
            new_button.text_size = super().width, None  # Set width of text to sidebar width
            self.btn_list.append(new_button)
            self.add_widget(new_button)
