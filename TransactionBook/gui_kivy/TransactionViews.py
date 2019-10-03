from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.window import Window
from TransactionBook.gui_kivy.generic.MsgBox import MsgBox
from TransactionBook.gui_kivy.generic.datepicker import DatePicker
from TransactionBook.gui_kivy.generic.ListPicker import ListPicker
from datetime import datetime
from TransactionBook.gui_kivy.generic.InputBox import InputBox
from TransactionBook.gui_kivy.generic.TextCheck import TextCheck
from TransactionBook.gui_kivy.generic.MultiSelectPopUp import MultiSelectPopUp


class TransactionItemGrid(GridLayout):
    """
    Date | Account | Amount | Description | Category | Edit-Button
    """
    def __init__(self, date, account, amount, description, category, ctrl, index=None, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.index = index
        self.ctrl = ctrl

        if index == None:  # Heading row
            self.gui_el_date = Button(text=date, size_hint_x=None, width=150)
            self.gui_el_date.bind(on_press=self.filter_date_callback)
            self.gui_el_account = Button(text=account)
            self.gui_el_account.bind(on_press=self.filter_account_callback)
            self.gui_el_amount = Button(text=amount, size_hint_x=None, width=150)
            self.gui_el_description = Button(text=description)
            self.gui_el_category = Button(text=category)
            self.gui_el_category.bind(on_press=self.filter_category_callback)
            btn = Button(text="N", size_hint_x=None, width=90)
            btn.bind(on_press=self.filter_itemcount_callback)

        else:  # Data row
            btn = Button(text="Edit", size_hint_x=None, width=90)
            btn.bind(on_press=self.edit_callback)
            self.gui_el_date = Label(text=date, size_hint_x=None, width=150)
            self.gui_el_account = Label(text=account)
            self.gui_el_amount = Label(text=amount, size_hint_x=None, width=150)
            self.gui_el_description = Label(text=description)
            self.gui_el_category = Label(text=category)

        self.add_widget(self.gui_el_date)
        self.add_widget(self.gui_el_account)
        self.add_widget(self.gui_el_amount)
        self.add_widget(self.gui_el_description)
        self.add_widget(self.gui_el_category)
        self.add_widget(btn)

    def edit_callback(self, _):
        self.ctrl.popup = TransactionDetailsPopUp(ctrl=self.ctrl, index=self.index)

    def filter_date_callback(self, _):
        DateSelectionPopup(self.ctrl)

    def filter_account_callback(self, _):
        topic = self.ctrl.model.ACCOUNT
        options = self.ctrl.model.accounts
        self._multi_select_filter(topic, options)

    def filter_category_callback(self, _):
        topic = self.ctrl.model.CATEGORY
        options = self.ctrl.model.categories
        self._multi_select_filter(topic, options)

    def _multi_select_filter(self, topic, options):
        my_filter = self.ctrl.transaction_filter

        def cb(new_selected_list):
            my_filter.filter_select[topic] = new_selected_list
            self.ctrl.update()
        callback = cb
        selection = my_filter.check_if_selected(topic, options)
        MultiSelectPopUp(title=topic, option_list=options, option_init=selection, callback=callback)

    def filter_itemcount_callback(self, _):
        def cb(text):
            tc = TextCheck(text)
            if tc.check_integer():
                self.ctrl.transaction_filter.set_max_number_of_elements(int(text), True)
                self.ctrl.update()
            else:
                MsgBox("The entered value is not an integer and will be ignored")
        n = self.ctrl.transaction_filter.max_number_of_elements
        InputBox(callback=cb, title="Enter maximal rows which are shown", text=f"{n}", size=(600, 200))


class TransactionList(GridLayout):
    """
    Transaction
    Transaction
    ...
    """
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.spacing = 10
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.ctrl = ctrl
        self.filter_initialized = False

    def update(self):
        # Init filter
        if not self.filter_initialized and self.ctrl.model.years():
            years = self.ctrl.model.years()
            self.ctrl.transaction_filter.set_max_number_of_elements(50, True)
            if years:
                self.ctrl.transaction_filter.select_date_range(self.ctrl.model.DATE,
                                                               datetime(min(years), 1, 1),
                                                               datetime(max(years), 12, 31))
                # Select all categories
                for cat in self.ctrl.model.categories:
                    self.ctrl.transaction_filter.select(self.ctrl.model.CATEGORY, cat)
                # Select all categories
                for acc in self.ctrl.model.accounts:
                    self.ctrl.transaction_filter.select(self.ctrl.model.ACCOUNT, acc)
            self.filter_initialized = True

        # Renew GUI elements
        self.clear_widgets()
        model = self.ctrl.model
        heading = TransactionItemGrid(model.DATE,
                                      model.ACCOUNT,
                                      model.AMOUNT,
                                      model.DESCRIPTION,
                                      model.CATEGORY,
                                      ctrl=self.ctrl,
                                      index=None,
                                      size_hint_y=None,
                                      height=40)
        self.add_widget(heading)
        data = self.ctrl.transaction_filter.filter(self.ctrl.model.get_data())
        for index in reversed(data.index):
            row = data.loc[index]
            btn = TransactionItemGrid(row[self.ctrl.model.DATE].strftime(model.DATE_TIME_FORMAT),
                                      str(row[self.ctrl.model.ACCOUNT]),
                                      str(row[self.ctrl.model.AMOUNT]) + model.CURRENCY,
                                      str(row[self.ctrl.model.DESCRIPTION]),
                                      str(row[self.ctrl.model.CATEGORY]),
                                      ctrl=self.ctrl,
                                      index=index,
                                      size_hint_y=None, height=40)
            self.add_widget(btn)


class TransactionDetails(AnchorLayout):
    """
    Date: in date
    Account: in account
    ...
    """
    def __init__(self, ctrl, index=None, **kwargs):
        super().__init__(**kwargs)
        self.anchor_y = 'top'
        self.ctrl = ctrl
        self.index = index  # Only used when a transaction is edited and not created!

        self.grid = GridLayout()
        self.grid.cols = 2
        self.grid.spacing = 10
        self.grid.size_hint_y = None
        self.grid.bind(minimum_height=self.setter('height'))
        self.grid.row_default_height = 50

        # Input data
        self.grid.label_date = Label(text="Date:")
        self.grid.input_date = DatePicker()
        self.grid.label_acc = Label(text="Account:")
        self.grid.input_acc = ListPicker(ctrl.model.accounts, add_callback=self.cb_add_account, topic="Account")
        self.grid.label_amount = Label(text="Amount:")
        self.grid.input_amount = TextInput(text="", multiline=False, input_type='number')
        self.grid.label_category = Label(text="Category:")
        self.grid.input_category = ListPicker(self.ctrl.model.categories,
                                              add_callback=self.cb_add_category,
                                              topic="Category")

        self.grid.label_description = Label(text="Description:")
        self.grid.input_description = TextInput(text="", multiline=False)

        # Buttons:
        self.grid.button_cancel = Button(text="Cancel")
        self.grid.button_cancel.bind(on_press=self.cancel_callback)
        self.grid.button_save = Button(text="Save")
        self.grid.button_save.bind(on_press=self.save_callback)
        self.grid.button_delete = Button(text="Delete")
        self.grid.button_delete.bind(on_press=self.delete_callback)

        self.add_widget(self.grid)
        self.update()

    def cb_add_category(self, text):
        # Add category to model
        self.ctrl.model.categories.append(text)
        # Update GUI element to take new category into account
        self.grid.input_category = ListPicker(self.ctrl.model.categories,
                                              add_callback=self.cb_add_category,
                                              topic="Category")
        # Write category text in text box
        self.grid.input_category.text = text
        self.update()

    def cb_add_account(self, text):
        self.ctrl.model.accounts.append(text)
        # Update GUI element to take new category into account
        self.grid.input_acc = ListPicker(self.ctrl.model.accounts,
                                         add_callback=self.cb_add_account,
                                         topic="Account")
        self.grid.input_acc.text = text
        self.update()

    def update(self):
        if self.index != None:  # The transaction is not new -> fill fields with data
            model = self.ctrl.model
            data = model.get_data()
            row = data.loc[self.index]
            self.grid.input_date.text = row[self.ctrl.model.DATE].strftime(model.DATE_TIME_FORMAT)
            self.grid.input_acc.text = str(row[self.ctrl.model.ACCOUNT])
            self.grid.input_amount.text = str(row[self.ctrl.model.AMOUNT])
            self.grid.input_description.text = str(row[self.ctrl.model.DESCRIPTION])
            self.grid.input_category.text = str(row[self.ctrl.model.CATEGORY])

        self.grid.clear_widgets()
        self.grid.add_widget(self.grid.label_date)
        self.grid.add_widget(self.grid.input_date)
        self.grid.add_widget(self.grid.label_acc)
        self.grid.add_widget(self.grid.input_acc)
        self.grid.add_widget(self.grid.label_amount)
        self.grid.add_widget(self.grid.input_amount)
        self.grid.add_widget(self.grid.label_category)
        self.grid.add_widget(self.grid.input_category)
        self.grid.add_widget(self.grid.label_description)
        self.grid.add_widget(self.grid.input_description)

        # Buttons:
        self.grid.add_widget(self.grid.button_cancel)
        if self.index != None:
            additional_grid = GridLayout(cols=2)
            additional_grid.add_widget(self.grid.button_delete)
            additional_grid.add_widget(self.grid.button_save)
            self.grid.add_widget(additional_grid)
        else:
            self.grid.add_widget(self.grid.button_save)

    def cancel_callback(self, _):
        self.ctrl.update()

    def _check_input(self):
        amount_str = self.grid.input_amount.text
        return TextCheck(amount_str).check_float()

    def save_callback(self, _):
        if self._check_input():
            print(self.grid.input_category.text)
            if self.index != None:
                print(self.index)
                print(self.ctrl.model.get_data())
                self.ctrl.model.edit_transaction(self.index,
                                                 self.grid.input_date.text,
                                                 self.grid.input_acc.text,
                                                 self.grid.input_description.text,
                                                 float(self.grid.input_amount.text),
                                                 self.grid.input_category.text)
            else:
                self.ctrl.model.new_transaction(self.grid.input_date.text,
                                                self.grid.input_acc.text,
                                                self.grid.input_description.text,
                                                float(self.grid.input_amount.text),
                                                self.grid.input_category.text)
            self.ctrl.update()
        else:
            MsgBox("The entered amount is not valid.\nThe decimal separator is \".\"")

    def delete_callback(self, _):
        # ToDo: Implement additional question if the user is sure to delete the transaction
        self.ctrl.model.delete_transaction(self.index)
        self.ctrl.update()


class TransactionDetailsPopUp(Popup):
    pHint_x = NumericProperty(0.7)
    pHint_y = NumericProperty(0.7)
    pHint = ReferenceListProperty(pHint_x, pHint_y)

    def __init__(self, ctrl, index=None, **kwargs):
        super().__init__(**kwargs)
        self.content = TransactionDetails(ctrl, index=index)
        self.title = "Transaction"

        self.size_hint = self.pHint
        Window.release_all_keyboards()
        self.open()


class DateSelectionDetails(AnchorLayout):
    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.anchor_y = 'top'
        self.ctrl = ctrl

        self.grid = GridLayout()
        self.grid.cols = 2
        self.grid.spacing = 10
        self.grid.size_hint_y = None
        self.grid.bind(minimum_height=self.setter('height'))
        self.grid.row_default_height = 50

        # Input data
        self.grid.label_date_from = Label(text="Date from:")
        self.grid.input_date_from = DatePicker()
        self.grid.label_date_to = Label(text="Date to:")
        self.grid.input_date_to = DatePicker()
        self.grid.button_all = Button(text="All dates")
        self.grid.button_all.bind(on_press=self.btn_all_cb)
        self.grid.button_ok = Button(text="Ok")
        self.grid.button_ok.bind(on_press=self.btn_ok_cb)
        self.add_widget(self.grid)
        self.update()

    def update(self):
        self.grid.clear_widgets()
        # Set dates to current filter values
        date_from = self.ctrl.transaction_filter.get_filter_date_from(self.ctrl.model.DATE)
        date_to = self.ctrl.transaction_filter.get_filter_date_to(self.ctrl.model.DATE)
        date_from_txt = date_from.strftime(self.ctrl.model.DATE_TIME_FORMAT)
        date_to_txt = date_to.strftime(self.ctrl.model.DATE_TIME_FORMAT)
        self.grid.input_date_from.text = date_from_txt
        self.grid.input_date_to.text = date_to_txt

        # Add GUI elements
        self.grid.add_widget(self.grid.label_date_from)
        self.grid.add_widget(self.grid.input_date_from)
        self.grid.add_widget(self.grid.label_date_to)
        self.grid.add_widget(self.grid.input_date_to)
        self.grid.add_widget(self.grid.button_all)
        self.grid.add_widget(self.grid.button_ok)

    def btn_all_cb(self, _):
        years = self.ctrl.model.years()
        date_from = datetime(min(years), 1, 1)
        date_to = datetime(max(years), 12, 31)
        date_from_txt = date_from.strftime(self.ctrl.model.DATE_TIME_FORMAT)
        date_to_txt = date_to.strftime(self.ctrl.model.DATE_TIME_FORMAT)
        self.grid.input_date_from.text = date_from_txt
        self.grid.input_date_to.text = date_to_txt

    def btn_ok_cb(self, _):
        date_from_txt = self.grid.input_date_from.text
        date_to_txt = self.grid.input_date_to.text
        date_from = datetime.strptime(date_from_txt, self.ctrl.model.DATE_TIME_FORMAT)
        date_to = datetime.strptime(date_to_txt, self.ctrl.model.DATE_TIME_FORMAT)
        self.ctrl.transaction_filter.select_date_range(self.ctrl.model.DATE,
                                                       date_from,
                                                       date_to)
        self.ctrl.update()


class DateSelectionPopup(Popup):
    pHint_x = NumericProperty(0.7)
    pHint_y = NumericProperty(0.7)
    pHint = ReferenceListProperty(pHint_x, pHint_y)

    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.content = DateSelectionDetails(ctrl)
        self.title = "Date selection"
        ctrl.popup = self

        self.size_hint = self.pHint
        Window.release_all_keyboards()
        self.open()



