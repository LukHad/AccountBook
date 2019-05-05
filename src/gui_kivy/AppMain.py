from kivy.app import App
from src.gui_kivy.Display import Display


class AppMain(App):
    def build(self):
        return Display()


if __name__ == '__main__':
    AppMain().run()
