"""
Zadanie 9.4
Zadanie bez precyzyjnej treści - raczej zrób podobnie w swojej "bibliotece".

Poza routingiem i słownikiem JSONa (konkretniej "viewed") raczej nie wiele sie zmieniło. Poprawione nazewnictwo.

Dodałem "id" do update_episode() gdyz bez tego trzeba bylo zawsze wpisac id przy PUT

Dodałem tez sciezke przy zapisie i odczycie pliku JSON z danego folderu.
Zrobione jako klasa - tak dla treningu :)

Obsluga bledow jest przez flaskowe "abort".
"""

import os
from flask import Flask, jsonify, abort, make_response, request

from models import episodes


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'developmentOnlySecretKey')

@app.route("/api/v2/mando/", methods=["GET"])
def get_episodes_list():
    return jsonify(episodes.all())


@app.route("/api/v2/episode/<int:episode_id>", methods=["GET"])
def get_single_episode(episode_id):
    episode = episodes.get(episode_id)
    if not episode:
        abort(404)
    return jsonify({"episode": episode})


@app.errorhandler(400)
def validate_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.errorhandler(404)
def find_episode(error):
    return make_response(jsonify({'error': 'Episode not found', 'status_code': 404}), 404)


@app.route("/api/v2/mando/", methods=["POST"])
def create_episode():
    if not request.json or not 'title' in request.json:
        abort(400)
    episode = {
        'id': episodes.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'viewed': False
    }
    episodes.create(episode)
    return jsonify({'episode': episode}), 201


@app.route("/api/v2/episode/<int:episode_id>", methods=['DELETE'])
def delete_episode(episode_id):
    result = episodes.delete(episode_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v2/episode/<int:episode_id>", methods=["PUT"])
def update_episode(episode_id):
    episode = episodes.get(episode_id)
    if not episode:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        # additionally "id" to not necessarily define once again id with update (PUT)
        'id' in data and not isinstance(data.get('id'), int),

        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'viewed' in data and not isinstance(data.get('viewed'), bool)
    ]):
        abort(400)
    episode = {
        # additionally "id" to not necessarily define once again id with update (PUT)
        'id': data.get('id', episode['id']),

        'title': data.get('title', episode['title']),
        'description': data.get('description', episode['description']),
        'viewed': data.get('viewed', episode['viewed'])
    }
    episodes.update(episode_id, episode)
    return jsonify({'episode': episode})


if __name__ == "__main__":
    app.run(debug=True)