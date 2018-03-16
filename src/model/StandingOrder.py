class StandingOrder:
    next_id = 0

    def __init__(
        self, src_acc_id, target_acc_id, amount, date, interval_months,
        categorie, description, bool_income
    ):
        self.id = StandingOrder.next_id
        StandingOrder.next_id += 1
        self.src_acc_id = src_acc_id
        self.target_acc_id = target_acc_id
        if amount < 0:  # tmp
            print("Warning: amount in StandinOrders"
                  "should always be greater than 0")  # tmp
        self.amount = amount  # is always > 0 !
        self.date = date
        self.interval_months = interval_months
        self.categorie = categorie
        self.description = description
        # bool_income will be used to calculate percentage of savings / income
        self.bool_income = bool_income

    def __repr__(self):
        return "Standing Order"
