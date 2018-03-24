import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, root, width, heigth):
        tk.Frame.__init__(self, root, bg='#CCC',
                          borderwidth=2,
                          width=width,
                          height=heigth)
        self.pack(expand=False, fill='both', side='left', anchor='nw')
        self.width = width

    def add(self, caption, cb):
        print(self.width)
        button = tk.Button(self, text=caption, command=cb)
        button.grid(row=0, column=0, sticky='NW')
