from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

current_path = os.path.abspath(os.getcwd() + "/books.db")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{current_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

all_books = []


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title


db.create_all()


@app.route('/')
def home():
    return render_template('index.html', books=Book)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        db.session.add(Book(title=request.form.get('name'),
                            author=request.form.get('author'),
                            rating=request.form.get('rating')))
        db.session.commit()
        return redirect(url_for('home'))
    print(all_books)
    return render_template('add.html')


@app.route("/edit/<id_book>", methods=['POST', 'GET'])
def edit(id_book):
    if request.method == 'POST':
        book = Book.query.get(id_book)
        book.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book = Book.query.get(id_book)
    return render_template('edit.html', book=book)


@app.route('/delete/<id_book>')
def delete(id_book):
    book = Book.query.get(id_book)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
