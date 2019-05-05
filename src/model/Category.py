class Category:
    next_id = 0

    def __init__(self, name):
        self.id = Category.next_id
        Category.next_id += 1
        self.name = name
