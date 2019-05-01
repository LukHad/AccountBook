from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from src.Controller import Controller


class Sidebar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.width = 100
        self.btn_list = []
        self.update()

    def update(self):
        button_list = Controller.request_account_name_list()

        # Clear button list
        for btn in self.btn_list:
            self.remove_widget(btn)
        self.btn_list = []
        # Add new buttons
        for btn in button_list:
            new_button = Button(text=btn, width=100)
            self.btn_list.append(new_button)
            self.add_widget(new_button)


class DetailsPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Display(FloatLayout):
    """
    Sidebar | DetailsPage
    """
    SIDEBAR_WIDTH = 0.2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sidebar = Sidebar(size_hint=(Display.SIDEBAR_WIDTH, 1))
        details = DetailsPage()
        self.add_widget(sidebar)
        self.add_widget(details)


class MainPageApp(App):
    def build(self):
        return Display()


if __name__ == '__main__':
    MainPageApp().run()
