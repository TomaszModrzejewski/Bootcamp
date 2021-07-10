from flask import request, render_template, redirect, url_for
from main import app
from app.forms import BooksForm
from app.models import books


@app.route("/books/", methods=["GET", "POST"])
def books_list():
    books.create_table()
    form = BooksForm()
    book_list = books.select_all('books')
    error = ""

    if request.method == "POST":
        if form.validate_on_submit():
            books.add_book(list(form.data.values())[0:5])
        return redirect(url_for("books_list"))

    return render_template("books.html", form=form, books=book_list, error=error)


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = books.select_book('books', id=book_id)
    table_headers = ['title', 'author', 'year', 'genre', 'done']
    book_dict = dict(zip(table_headers, book[0][1:]))
    form = BooksForm(data=book_dict)

    if request.method == "POST":
        form = BooksForm()
        data = list(form.data.values())
        data_dict = dict(zip(table_headers, data))
        if request.form['btn'] == 'Zapisz':
            books.update('books', book_id, data_dict)
        if request.form['btn'] == 'Usuń':
            books.delete_book('books', id=book_id)

        return redirect(url_for("books_list"))

    return render_template("book.html", form=form, book_id=book_id)