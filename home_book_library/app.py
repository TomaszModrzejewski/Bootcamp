from flask import Flask, jsonify, abort, make_response, request
from models import library


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/library/", methods=["GET", "POST"])
def books_list_api_v1():
    if request.method == "GET":
        return jsonify(library.all())

    if not request.json or 'title' not in request.json:
        abort(400)
    book = {
        'id': library.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'author': request.json['author'],
        'done': False
    }
    library.create(book)
    return jsonify({'book': book}), 201


@app.route("/api/v1/book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = library.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.route("/api/v1/book/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = library.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/book/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = library.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    book = {
        'title': data.get('title', book['title']),
        'description': data.get('description', book['description']),
        'author': data.get('author', book['author']),
        'done': data.get('done', book['done'])
    }
    library.update(book_id, book)
    return jsonify({'book': book})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


if __name__ == "__main__":
    app.run(debug=True)
