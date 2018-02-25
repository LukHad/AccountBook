class Transaction:
    next_id = 0
    def __init__(self, src_acc_id, target_acc_id, amount, date,
        categorie, description, bool_income
        ):
        self.id = Transaction.next_id
        Transaction.next_id += 1
        self.src_acc_id = src_acc_id
        self.target_acc_id = target_acc_id
        self.amount = amount
        self.date = date
        self.categorie = categorie
        self.description = description
        self.bool_income = bool_income #will be used to calculate percentage of savings / income
