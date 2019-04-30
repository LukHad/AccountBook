# http://code.activestate.com/recipes/578887-text-widget-width-and-height-in-pixels-tkinter/
import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, master, width=0, height=0, **kwargs):
        self.width = width
        self.height = height
        tk.Frame.__init__(self, master, width=self.width, height=self.height)
        self.listbox = tk.Listbox(self, **kwargs)
        self.listbox.pack(expand=tk.YES, fill=tk.BOTH)
        self.listbox.config(selectmode=tk.SINGLE,
                            borderwidth=0,
                            selectborderwidth=0,
                            highlightthickness=0,
                            font=("Arial", 16))

    def pack(self, *args, **kwargs):
        tk.Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        tk.Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)

    def insert(self, *args):
        self.listbox.insert(*args)

    def add_command(self, command):
        self.listbox.bind('<<ListboxSelect>>', command)

    def selection_id(self):
        # retruns the selected entries integer id
        tupel = self.listbox.curselection()
        return [i for i in tupel][0]
