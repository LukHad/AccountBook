from kivy.uix.scrollview import ScrollView


class Details(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = None
        #with self.canvas.before:  # add background color
         #   Color(1, 1, 1, 1)
          #  self.rect = Rectangle(size=self.size,
           #                       pos=self.pos)

    def update(self, content):
        self.clear_widgets()
        self.content = content
        self.add_widget(self.content)

