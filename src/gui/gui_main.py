import tkinter as tk


class gui_main(tk.Frame):
    def __init__(self, root=None):
        self.root = root
        tk.Frame.__init__(self, root)
        root.minsize(width=1024, height=600)
        self.root.title("Main Window Title")
        self.init_menubar()
        self.init_window()

    def init_menubar(self):
        # create main menubar instance
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # <start> File
        # create menubar submenu
        filemenu = tk.Menu(menubar)
        # fill submenu
        filemenu.add_command(label="Open", command=self.cb_dummy)
        filemenu.add_command(label="Save", command=self.cb_dummy)
        filemenu.add_command(label="Save As", command=self.cb_dummy)
        filemenu.add_command(label="Exit", command=self.cb_menubar_exit)
        # add submenu to menubar
        menubar.add_cascade(label="File", menu=filemenu)
        # <end> File

        # <start> View
        viewmenu = tk.Menu(menubar)
        viewmenu.add_command(label="Data input", command=self.cb_dummy)
        viewmenu.add_command(label="Data view", command=self.cb_dummy)
        # add submenu to menubar
        menubar.add_cascade(label="View", menu=viewmenu)
        # <end> View

    def cb_menubar_exit(self):
        exit()

    def cb_dummy(self):
        # filemenu.entryconfigure(pos, label="Clicked!")
        print("Pressed")

    # test:
    def init_window(self):
        # allowing the widget to take the full space of the root window
        self.pack(fill=tk.BOTH, expand=1)
        # creating a button instance
        quitButton = tk.Button(self, text="Quit", command = self.cb_menubar_exit)
        # placing the button on my window
        quitButton.place(x=0, y=0)


root = tk.Tk()
app = gui_main(root)
app.mainloop()
