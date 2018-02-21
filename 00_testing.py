from Account import Account

acc = Account(11)

acc.deposit(10)
acc.deposit(23)

acc.print_transactions()

print(acc.balance)
