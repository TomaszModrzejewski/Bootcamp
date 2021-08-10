import json


class Library:
    def __init__(self):
        try:
            with open("library.json", "r") as f:
                self.library = json.load(f)
        except FileNotFoundError:
            self.library = []

    def all(self):
        return self.library

    def get(self, id):
        book = [book for book in self.all() if book['id'] == id]
        if book:
            return book[0]
        return None

    def create(self, data):
        data.pop('csrf_token')
        self.library.append(data)

    def save_all(self):
        with open("library.json", "w") as f:
            json.dump(self.library, f)

    def update(self, id, data):
        book = self.get(id)
        if book:
            index = self.library.index(book)
            self.library[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id)
        if book:
            self.library.remove(book)
            self.save_all()
            return True
        return False


library = Library()
