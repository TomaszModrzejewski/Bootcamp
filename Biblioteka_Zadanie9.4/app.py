from flask import Flask, jsonify, abort, make_response, request
from models import bookstore

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found", "status_code": 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request", "status_code": 400}), 400)


@app.route("/api/v1/library/", methods=["GET"])
def library_list_api_v1():
    return jsonify(bookstore.all())


@app.route("/api/v1/library/", methods=["POST"])
def create_book():
    if not request.json or any([
        not "title",
        not "author",
        not "pages",
        not "price"
    ]) in request.json:
        abort(400)
    book = {
        "id": bookstore.all()[-1]["id"] + 1,
        "title": request.json["title"],
        "author": request.json["author"],
        "pages": request.json["pages"],
        "description": request.json.get("description", ""),
        "price": request.json["price"]
    }
    bookstore.create(book)
    return jsonify({"book": book}), 201


@app.route("/api/v1/library/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = bookstore.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.route("/api/v1/library/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    result = bookstore.delete(book_id)
    if not result:
        abort(404)
    return jsonify({"result": result})


@app.route("/api/v1/library/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = bookstore.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        "title" in data and not isinstance(data.get("title"), str),
        "author" in data and not isinstance(data.get("author"), str),
        "pages" in data and not isinstance(data.get("pages"), int),
        "description" in data and not isinstance(data.get("description"), str),
        "price" in data and not isinstance(data.get("price"), float)
    ]):
        abort(400)

    book = {
        "title": data.get("title", book["title"]),
        "author": data.get("author", book["author"]),
        "pages": data.get("pages", book["pages"]),
        "description": data.get("description", book["description"]),
        "price": data.get("price", book["price"])
    }
    bookstore.update(book_id, book)
    return jsonify({"book": book})


if __name__ == "__main__":
    app.run(debug=True)
