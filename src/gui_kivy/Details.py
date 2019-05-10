from kivy.uix.scrollview import ScrollView


class Details(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = None

    def update(self, content):
        self.clear_widgets()
        self.content = content
        self.add_widget(self.content)

