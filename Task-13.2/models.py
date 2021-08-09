import os
import json

SAVED_FOLDER_NAME = 'Saved'
FILE_NAME = "mando.json"
FILE_PATH = os.path.join(SAVED_FOLDER_NAME, FILE_NAME)


class File:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_from_file(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            data = []


    def save_file(self, data):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(data, f)




class Todos(File):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todos = self.load_from_file()

    def all(self):
        return self.todos

    def get(self, id):
        todo = [todo for todo in self.all() if todo['id'] == id]
        if todo:
            return todo[0]
        return []

    def create(self, data):
        #data.pop('csrf_token')
        self.todos.append(data)
        self.save_all()

    def save_all(self):
        self.save_file(self.todos)

    def delete(self, id):
        todo = self.get(id)
        if todo:
            self.todos.remove(todo)
            self.save_all()
            return True
        return False

    def update(self, id, data):
        todo = self.get(id)
        if todo:
            index = self.todos.index(todo)
            self.todos[index] = data
            self.save_all()
            return True
        return False

episodes = Todos(file_path=FILE_PATH)
datas = File(file_path=FILE_PATH).load_from_file()