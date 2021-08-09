from app import app, db
from app.models import Book, Author


from app import app, db
from app.models import Book, Author, Status_Enum, Rental

@app.shell_context_processor
def make_shell_context():
   return {
       "db": db,
       "Book": Book,
       "Author": Author,
       "Status_Enum": Status_Enum,
       "Rental": Rental,
   }