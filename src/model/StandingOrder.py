class StandingOrder:
    next_id = 0

    def __init__(
        self, src_acc_id, target_acc_id, amount, date, interval_months,
        category, description
    ):
        self.id = StandingOrder.next_id
        StandingOrder.next_id += 1
        self.src_acc_id = src_acc_id
        self.target_acc_id = target_acc_id
        if amount < 0:  # tmp
            print("Warning: amount in StandinOrders"
                  "should always be greater than 0")  # tmp
        self.amount = amount  # is always > 0 !
        self.date = date  # of next transaction
        self.interval_months = interval_months
        self.category = category
        self.description = description

    def __repr__(self):
        return "Standing Order"
