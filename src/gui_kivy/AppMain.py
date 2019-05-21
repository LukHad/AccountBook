from kivy.app import App
from src.gui_kivy.DisplayController import DisplayController


class AppMain(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display_controller = DisplayController()

    def build(self):
        return self.display_controller

    def on_stop(self):
        self.display_controller.on_stop()

    def on_start(self):
        self.display_controller.on_start()


if __name__ == '__main__':
    AppMain().run()
