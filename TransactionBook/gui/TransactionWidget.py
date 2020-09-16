import sys

from PySide2.QtWidgets import QWidget, QMainWindow, QAction, QGridLayout, QTabWidget


class TransactionWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(TransactionWidget, self).__init__(*args, **kwargs)