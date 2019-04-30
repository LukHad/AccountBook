from . import Page


def accounts_page(self):
    acc_page = Page.Page(self,
                         width=self.SIDEBAR_WIDTH,
                         height=self.MAIN_WIN_HEIGTH
                         )
    acc_page.pack(side='left')
    print("accounts page initalized")
