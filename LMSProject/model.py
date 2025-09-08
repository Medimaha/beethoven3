# Book {id, title, price, copies}

class Book:
    def __init__(self, id=None, title='', price=1, copies=1):
        self.id = id
        self.title = title
        self.price = price
        self.copies = copies
    
    def __str__(self):
        return f'[{self.id}, {self.title}, {self.price}, {self.copies}]'

class Info:
    def __init__(self, val=0):
        self.val = val