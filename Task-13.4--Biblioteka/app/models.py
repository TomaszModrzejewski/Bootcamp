from app import db
import enum


class Author(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    books = db.relationship("Book", backref="author_name")

    def __str__(self):
        return f"Author {self.name}"


class Status_Enum(enum.Enum):
    available = 'available'
    not_available = 'not_available'


class Rental(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status_Enum), default=Status_Enum.available)
    books = db.relationship("Book", backref="rental_status")

    def __str__(self):
        return f"Book is {self.status}"


class Book(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(100))
    quantity = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    rental_id = db.Column(db.Integer, db.ForeignKey('rental.id'))

    def __str__(self):
        return f"Book {self.tittle}"

    def get_author(self):
        author = Author.query.filter_by(id=self.author_id).first()
        return author.name

    def get_rental_status(self):
        rental_status = Rental.query.filter_by(id=self.rental_id).first()
        return rental_status.status.value