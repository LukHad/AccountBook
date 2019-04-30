import tkinter as tk
from .Sidebar import Sidebar
# from .Page import Page
from .accounts_page import accounts_page


class AppFrame(tk.Frame):
    def __init__(self):
        # set main window constants
        self.MAIN_WIN_WIDTH = 1024
        self.MAIN_WIN_HEIGTH = 600
        self.SIDEBAR_WIDTH = 0.18 * self.MAIN_WIN_WIDTH
        # init main window
        self.parent = tk.Tk()
        tk.Frame.__init__(self, self.parent)
        self.parent.minsize(width=self.MAIN_WIN_WIDTH,
                            height=self.MAIN_WIN_HEIGTH)
        self.parent.maxsize(width=self.MAIN_WIN_WIDTH,
                            height=self.MAIN_WIN_HEIGTH)
        self.parent.title("Account Book")
        # init window structure
        self.init_menubar()
        self.sidebar = self.init_sidebar()
        # create container for all pages and init constant pages
        self.pages = []
        self.add_data_pages()

    def init_menubar(self):
        # create main menubar instance
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

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

        # <start> Pages
        pagesmenu = tk.Menu(menubar)
        pagesmenu.add_command(label="Edit Page", command=self.cb_dummy)
        pagesmenu.add_command(label="Add Page", command=self.cb_dummy)
        # add submenu to menubar
        menubar.add_cascade(label="Pages", menu=pagesmenu)
        # <end> View

    def init_sidebar(self):
        sidebar = Sidebar(self.parent,
                          width=self.SIDEBAR_WIDTH,
                          height=self.MAIN_WIN_HEIGTH,
                          borderwidth=0, bg='#CCC')
        sidebar.pack(side='left')
        sidebar.insert(tk.END, "Accounts")  # tmp
        sidebar.insert(tk.END, "Standing Orders")  # tmp
        sidebar.insert(tk.END, "Categories")  # tmp
        sidebar.add_command(self.cb_sidebar)
        return sidebar

    def add_data_pages(self):
        accounts_page(self)

    def add_page(self):
        print("dummy")

    def cb_sidebar(self, _):
        print(self.sidebar.selection_id())

    def cb_menubar_exit(self):
        exit()

    def cb_dummy(self, event=None):
        # filemenu.entryconfigure(pos, label="Clicked!")
        print("Pressed", event)
