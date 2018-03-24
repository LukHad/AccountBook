import tkinter as tk
from Sidebar import Sidebar

MAIN_WIN_WIDTH = 1024
MAIN_WIN_HEIGTH = 600
MAIN_SIDEBAR_WIDTH_PERCENTAGE = 0.2  # % of main widow width


class gui_main(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        tk.Frame.__init__(self, self.root)
        self.root.minsize(width=MAIN_WIN_WIDTH, height=MAIN_WIN_HEIGTH)
        # root.maxsize(width=MAIN_WIN_WIDTH, height=MAIN_WIN_HEIGTH)
        self.root.title("Account Book")
        self.init_menubar()
        self.sidebar = Sidebar(self.root,
                               int(MAIN_SIDEBAR_WIDTH_PERCENTAGE*MAIN_WIN_WIDTH),
                               MAIN_WIN_HEIGTH)

        self.sidebar.add("MyButton", self.cb_dummy)

        #self.sidebar = self.init_sidebar()
        self.main_area = self.init_main_area()

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

    # def init_sidebar(self):
    #     # initialize sidebar
    #     sidebar = tk.Frame(self.root, bg='#CCC', # relief='sunken',
    #                        borderwidth=2,
    #                        width=MAIN_SIDEBAR_WIDTH_PERCENTAGE*MAIN_WIN_WIDTH,
    #                        height=MAIN_WIN_HEIGTH)
    #     sidebar.pack(expand=False, fill='both', side='left', anchor='nw')
    #     return sidebar

    def init_main_area(self):
        # main content area
        main_area = tk.Frame(self.root, bg='white',
                             width=(1-MAIN_SIDEBAR_WIDTH_PERCENTAGE)*MAIN_WIN_WIDTH,
                             height=MAIN_WIN_HEIGTH)
        main_area.pack(expand=True, fill='both', side='right')
        return main_area

    def cb_menubar_exit(self):
        exit()

    def cb_dummy(self):
        # filemenu.entryconfigure(pos, label="Clicked!")
        print("Pressed")

    # test:
    # def init_window(self):
    #     # allowing the widget to take the full space of the root window
    #     self.pack(fill=tk.BOTH, expand=1)
    #     # creating a button instance
    #     quitButton = tk.Button(self, text="Quit", command=self.cb_menubar_exit)
    #     # placing the button on my window
    #     quitButton.place(x=0, y=0)


app = gui_main()
app.mainloop()
