class Categorie:
    next_id = 0
    def __init__(self, name):
        self.id = Categorie.next_id
        Categorie.next_id += 1
        self.name = name
