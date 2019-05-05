from kivy.app import App
from src.gui_kivy.DisplayController import DisplayController


class AppMain(App):
    def build(self):
        return DisplayController()


if __name__ == '__main__':
    AppMain().run()
