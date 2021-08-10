from flask import Flask, request, redirect, url_for, render_template
from app import app, db
from app.models import Book, Author, Rental
from app.forms import BookForm


@app.route("/books/", methods=["GET", "POST"])
def book_list():
    form = BookForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            all_authors_names = []
            all_authors_results = Author.query.all()
            for author in all_authors_results:
                all_authors_names.append(author.name)
            if form.data["author"] in all_authors_names:
                pass
            else:
                new_author = Author(name=form.data["author"])
                db.session.add(new_author)
                db.session.commit()
            author_from_form = Author.query.filter_by(name=form.data['author']).first()
            rental_from_form = Rental.query.filter_by(status=form.data['status']).first()
            new_book = Book(tittle=form.data["tittle"], quantity=form.data['quantity'], author_id=author_from_form.id,
                            rental_id=rental_from_form.id)
            db.session.add(new_book)
            db.session.commit()
        return redirect((url_for("book_list")))
    return render_template("book.html", form=form, books=Book.query.all(), error=error)


@app.route("/books/edit/<int:id>", methods=["GET", "POST"])
def book_edit(id):
    book = Book.query.filter_by(id=id).first()
    author = Author.query.filter_by(id=book.author_id).first()
    rental = Rental.query.filter_by(id=book.rental_id).first()
    form = BookForm(data={
        'tittle': book.tittle,
        'author': author.name,
        'quantity': book.quantity,
        'status': rental.status,
        'csrf_token': 1234})
    if request.method == "POST":
        if form.validate_on_submit():
            all_authors_names = []
            all_authors_results = Author.query.all()
            for author in all_authors_results:
                all_authors_names.append(author.name)
            if form.data["author"] in all_authors_names:
                pass
            else:
                new_author = Author(name=form.data["author"])
                db.session.add(new_author)
                db.session.commit()
            author_from_form = Author.query.filter_by(name=form.data['author']).first()
            rental_from_form = Rental.query.filter_by(status=form.data['status']).first()
            book.tittle = form.data["tittle"]
            book.quantity = form.data['quantity']
            book.author_id = author_from_form.id
            book.rental_id = rental_from_form.id
            db.session.commit()
        return redirect((url_for("book_list")))
    return render_template("book_id.html", form=form, id=id, book=book)

@app.route("/books/<int:id>/delete", methods=["POST"])
def book_delete(id):
    book = Book.query.get(id=id)
    db.session.delete(book)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)