import json


class Library:
    def __init__(self):
        try:
            with open("booklibrary.json", "r") as f:
                items = json.load(f)
                sorted_items = sorted(items, key=lambda k: k["price"], reverse=True)
                self.allitems = sorted_items
        except FileNotFoundError:
            self.allitems = []

    def all(self):
        with open("booklibrary.json", "r") as f:
            items = json.load(f)
            self.allitems = sorted(items, key=lambda k: k["price"], reverse=True)
        return self.allitems

    def get(self, id):
        book = [book for book in self.all() if book["id"] == id]
        if book:
            return book[0]
        return []

    def create(self, data):
        self.allitems.append(data)
        self.save_all()

    def save_all(self):
        with open("booklibrary.json", "w") as f:
            json.dump(self.allitems, f)

    def update(self, id, data):
        book = self.get(id)
        if book:
            index = self.allitems.index(book)
            self.allitems[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id)
        if book:
            self.allitems.remove(book)
            self.save_all()
            return True
        return False


bookstore = Library()
