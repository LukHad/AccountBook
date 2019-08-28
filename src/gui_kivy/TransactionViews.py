from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.window import Window
from src.gui_kivy.generic.MsgBox import MsgBox
from src.gui_kivy.generic.datepicker import DatePicker
from src.gui_kivy.generic.ListPicker import ListPicker


class TransactionItemGrid(GridLayout):
    """
    Date | Account | Amount | Description | Category | Edit-Button
    """
    def __init__(self, date, account, amount, description, category, ctrl, index=None, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.index = index
        self.ctrl = ctrl
        self.label_date = Label(text=date, size_hint_x=None, width=150)
        self.label_account = Label(text=account)
        self.label_amount = Label(text=amount, size_hint_x=None, width=150)
        self.label_description = Label(text=description)
        self.label_category = Label(text=category)

        self.add_widget(self.label_date)
        self.add_widget(self.label_account)
        self.add_widget(self.label_amount)
        self.add_widget(self.label_description)
        self.add_widget(self.label_category)
        if index != None:
            btn_edit = Button(text="Edit", size_hint_x=None, width=90)
            btn_edit.bind(on_press=self.edit_callback)
            self.add_widget(btn_edit)
        else:
            btn_edit_dummy = Label(text="", size_hint_x=None, width=90)
            self.add_widget(btn_edit_dummy)

    def edit_callback(self, _):
        self.ctrl.popup = TransactionDetailsPopUp(ctrl=self.ctrl, index=self.index)


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

    def update(self):
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

        i = 0
        for index, row in self.ctrl.model.data.iterrows():
            btn = TransactionItemGrid(row[self.ctrl.model.DATE].strftime(model.DATE_TIME_FORMAT),
                                      str(row[self.ctrl.model.ACCOUNT]),
                                      str(row[self.ctrl.model.AMOUNT]) + model.CURRENCY,
                                      str(row[self.ctrl.model.DESCRIPTION]),
                                      str(row[self.ctrl.model.CATEGORY]),
                                      ctrl=self.ctrl,
                                      index=index,
                                      size_hint_y=None, height=40)
            self.add_widget(btn)
            if i > 100:  # ToDo Make listed transaction dynamic -> Introduce filter
                break
            i = i + 1


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
            row = model.data.loc[self.index]
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
        try:
            float(amount_str)
            return True
        except:
            return False

    def save_callback(self, _):
        if self._check_input():
            if self.index != None:
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



