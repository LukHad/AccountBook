#!/usr/bin/env python
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QTabWidget, QWidget, QAction, QToolBar, QFileDialog, \
                              QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from TransactionBook.gui.TransactionWidget import TransactionTableWidget, TransactionPopUp


class MainWindow(QMainWindow):

    def __init__(self, ctrl):
        super(MainWindow, self).__init__()
        self.ctrl = ctrl
        # Window settings
        # self.name = self.ctrl.get_loaded_file_name()
        # self.setWindowTitle(self.name)
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
        self.setWindowTitle(self.ctrl.get_loaded_file_name())

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
        # Add transaction
        add_action = QAction(QIcon('gui/icons/add.png'), "New", self)
        add_action.setToolTip("Add transaction")
        add_action.triggered.connect(self.cb_new_transaction_button)
        # Edit transaction
        edit_action = QAction(QIcon('gui/icons/edit.png'), "New", self)
        edit_action.setToolTip("Edit transaction")
        edit_action.triggered.connect(self.cb_edit_transaction_button)
        # Delete transaction
        delete_action = QAction(QIcon('gui/icons/delete.png'), "New", self)
        delete_action.setToolTip("Delete transaction")
        delete_action.triggered.connect(self.cb_delete_transaction_button)

        # add_action.setShortcut('Ctrl+Q')
        toolbar.addAction(add_action)
        toolbar.addAction(edit_action)
        toolbar.addAction(delete_action)

    def init_central_widget(self):
        tab_widget = QTabWidget()
        tab_widget.addTab(self.transaction_widget, self.transaction_widget.name)
        tab_widget.addTab(self.account_widget, "Accounts")

        self.setCentralWidget(tab_widget)

    def cb_new_transaction_button(self):
        self.popup = TransactionPopUp(self.ctrl)
        self.popup.show()

    def cb_edit_transaction_button(self):
        unique_row_list = self.__get_selected_rows()
        if len(unique_row_list) != 1:
            msg_box = QMessageBox()
            msg_box.setText("Please select only one transaction you want to edit in the table below")
            msg_box.exec_()
        else:
            selected_row = unique_row_list[0]
            self.ctrl.debug_print(selected_row)
            self.popup = TransactionPopUp(self.ctrl, edit_transaction_id=selected_row)
            self.popup.show()

    def cb_delete_transaction_button(self):
        unique_row_list = self.__get_selected_rows()
        if len(unique_row_list) < 1:
            msg_box = QMessageBox()
            msg_box.setText("Please select the transactions you want to delete in the table below")
            msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setText(f"Do you really want to delete the following table rows: {unique_row_list} ?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            answer = msg_box.exec_()
            if answer == QMessageBox.Yes:
                self.ctrl.event_delete_transaction(unique_row_list)

    def __get_selected_rows(self):
        # Get a list of all selected rows
        row_list = [item.row() for item in self.transaction_widget.table.selectionModel().selectedIndexes()]
        # Remove duplicates in case several cells of one row are selected
        unique_row_list = list(set(row_list))
        return unique_row_list

    def new_file(self):
        print("New File")

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self, self.tr("Open..."), self.tr(""), self.tr("*.csv"))[0]
        if file_path != '':
            # ToDo: Check if file is valid database
            self.ctrl.debug_print(f"View: Open {file_path}")
            self.ctrl.event_open_file(file_path)

    def save_file(self):
        if self.ctrl.get_file_path() is not None:
            self.ctrl.debug_print(f"View: Save file")
            self.ctrl.event_save_file()
        else:
            self.ctrl.debug_print(f"View: Redirection to save as...")
            self.save_as_file()

    def save_as_file(self):
        file_path = QFileDialog.getSaveFileName(self, self.tr("Save as..."), self.tr(""), self.tr("*.csv"))[0]
        if file_path != '':
            self.ctrl.debug_print(f"View: save as {file_path}")
            self.ctrl.event_save_file(file_path)

    def close_file(self):
        print("Close File")


