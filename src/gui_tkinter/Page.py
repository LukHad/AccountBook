import tkinter as tk


class Page(tk.Frame):
    def __init__(self, parent, width=0, height=0, **kwargs):
        self.width = width
        self.height = height
        tk.Frame.__init__(self, parent, width=self.width, height=self.height,
                          bg='LemonChiffon2')
        print("Page initalized")
