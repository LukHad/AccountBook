#!/usr/bin/env python
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QTabWidget, QWidget, QAction, QToolBar
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from TransactionBook.gui.TransactionWidget import TransactionTableWidget, NewTransactionPopUp


class MainWindow(QMainWindow):

    def __init__(self, ctrl):
        super(MainWindow, self).__init__()
        self.ctrl = ctrl
        # Window settings
        self.name = "Transaction Book"
        self.setWindowTitle(self.name)
        self.setMinimumSize(600, 400)
        self.resize(1500, 900)

        # Menu Bar
        self.init_menu_bar()

        # Toolbar
        self.init_toolbar()

        # Central Widgets
        self.transaction_widget = TransactionTableWidget(self.ctrl)
        self.account_widget = QWidget()
        self.init_central_widget()

        #
        self.popup = None

    def update_data(self):
        self.transaction_widget.update_data()


    def init_menu_bar(self):
        menu_bar = self.menuBar()
        # File Menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("New File", self, triggered=self.new_file))
        file_menu.addAction(QAction("Open...", self, triggered=self.open_file))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Save", self, triggered=self.save_file))
        file_menu.addAction(QAction("Save As...", self, triggered=self.save_as_file))
        file_menu.addSeparator()
        file_menu.addAction(QAction("Close File", self, triggered=self.close_file))
        file_menu.addAction("Exit", QApplication.quit)

    def init_toolbar(self):
        toolbar = self.addToolBar("Toolbar")
        add_action = QAction(QIcon('gui/icons/add.png'), "New", self)
        add_action.setToolTip("Add transaction")
        add_action.triggered.connect(self.cb_new_transaction_button)
        # add_action.setShortcut('Ctrl+Q')
        toolbar.addAction(add_action)

    def init_central_widget(self):
        tab_widget = QTabWidget()
        tab_widget.addTab(self.transaction_widget, self.transaction_widget.name)
        tab_widget.addTab(self.account_widget, "Accounts")

        self.setCentralWidget(tab_widget)

    def cb_new_transaction_button(self):
        self.popup = NewTransactionPopUp(self.ctrl, self)
        self.popup.show()

    def new_file(self):
        print("New File")

    def open_file(self):
        print("Open File")

    def save_file(self):
        print("Save")

    def save_as_file(self):
        print("Save As")

    def close_file(self):
        print("Close File")


