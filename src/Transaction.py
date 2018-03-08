class Transaction:
    next_id = 0

    def __init__(
        self, amount, date,
        categorie, description, bool_income
    ):
        self.id = Transaction.next_id
        Transaction.next_id += 1
        self.amount = amount
        self.date = date
        self.categorie = categorie
        self.description = description
        # bool_income will be used to calculate percentage of savings / income
        self.bool_income = bool_income
