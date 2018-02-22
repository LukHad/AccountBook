class Transaction:
    def __init__(self, id, src_acc_id, target_acc_id, amount, date,
        categorie, description, bool_income
        ):
        self.id = id
        self.src_acc_id = src_acc_id
        self.target_acc_id = target_acc_id
        self.amount = amount
        self.date = date
        self.categorie = categorie
        self.description = description
        self.bool_income = bool_income #will be used to calculate percentage of savings / income
