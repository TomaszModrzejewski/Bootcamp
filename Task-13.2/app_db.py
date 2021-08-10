"""
Zadanie 13.2
Bazujac na zad 9.4 dodano obsuge bazy danych SQLite

restore_all_from_JSON()  to dane z JSONa
nie ma opcji zapisu do JSONa z poziomu tej appki.
"""

import os
from flask import Flask, jsonify, abort, make_response, request

from modelsSQLite import episodes, tasks, load_episodes_JSON_backup



app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'developmentOnlySecretKey')



@app.errorhandler(400)
def validate_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.errorhandler(404)
def find_episode(error):
    return make_response(jsonify({'error': 'Episode or task not found', 'status_code': 404}), 404)




@app.route("/api/mando/epi/", methods=["GET"])
def get_episodes_list():
    return jsonify(episodes.select_all())


@app.route("/api/mando/task/", methods=["GET"])
def get_tasks_list():
    return jsonify(tasks.select_all())


@app.route("/api/mando/epi/<int:episode_id>", methods=["GET"])
def get_single_episode(episode_id):
    episode = episodes.select_where(id=episode_id)
    if not episode:
        abort(404)
    return jsonify({"episode": episode})


@app.route("/api/mando/task/<int:id>", methods=["GET"])
def get_single_task(id):
    task = tasks.select_where(id=id)
    if not task:
        abort(404)
    return jsonify({"task": task})


@app.route("/api/mando/task/<status>", methods=["GET"])
def get_task_by_status(status):
    task = tasks.select_task_by_status(status)
    if not task:
        abort(404)
    return jsonify({"task": task})


@app.route("/api/mando/epi/", methods=["POST"])
def create_episode():
    if not request.json or not 'title' in request.json:
        abort(400)

    data = request.json
    title = data.get('title')
    description = data.get('description')

    episode = (title, description)
    episodes.add_episode(episode)
    return jsonify({'episode': episode}), 201


@app.route("/api/mando/task/", methods=["POST"])
def create_task():
    if not request.json or not 'episode_id' in request.json:
        abort(400)

    data = request.json
    episode_id = data.get('episode_id')
    task = data.get('task')
    task_description = data.get('task_description')
    status = data.get('status')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    taski = (episode_id, task, task_description, status, start_date, end_date)

    tasks.add_task(taski)
    return jsonify({'task': taski}), 201

@app.route("/api/mando/epi/<int:episode_id>", methods=["PUT"])
def update_episode(episode_id):
    episode = episodes.select_where(id=episode_id)
    episode = episode[0]
    if not episode:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'id' in data and not isinstance(data.get('id'), int),
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
    ]):
        abort(400)

    title = data.get('title', episode[1])
    description = data.get('description', episode[2])
    
    episodes.update(id=episode_id, title=title, description=description)
    return jsonify({'episode': episode})


@app.route("/api/mando/task/<int:id>", methods=["PUT"])
def update_task(id):
    taski = tasks.select_where(id=id)
    taski = taski[0]
    if not taski:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'id' in data and not isinstance(data.get('id'), int),
        'episode_id' in data and not isinstance(data.get('episode_id'), int),
        'task' in data and not isinstance(data.get('task'), str),
        'task_description' in data and not isinstance(data.get('task_description'), str),
        'status' in data and not isinstance(data.get('status'), str),
        'start_date' in data and not isinstance(data.get('start_date'), str),
        'end_date' in data and not isinstance(data.get('end_date'), str)
        ]):
        abort(400)

    episode_id = data.get('episode_id', taski[1])
    task = data.get('task', taski[2])
    task_description = data.get('task_description',taski[3])
    status = data.get('status', taski[4])
    start_date = data.get('start_date', taski[5])
    end_date = data.get('end_date', taski[6])
    
    tasks.update(id=id, episode_id=episode_id, task=task, task_description=task_description, status=status, start_date=start_date, end_date=end_date)
    return jsonify({'task': taski})


@app.route("/api/mando/epi/<int:episode_id>", methods=['DELETE'])
def delete_episode(episode_id):
    result_1 = tasks.delete_where(episode_id=episode_id)
    result_2 = episodes.delete_where(id=episode_id)
    if not result_1 and not result_2:
        abort(404)
    return jsonify({'result': [result_1, result_2]})


@app.route("/api/mando/task/<int:id>", methods=['DELETE'])
def delete_task(id):
    result = tasks.delete_where(id=id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/mando/delete/", methods=['DELETE'])
def delete_all():
    tasks.delete_all()
    episodes.delete_all()
    return jsonify({'result': "Tables episodes and tasks cleared"})


@app.route("/api/mando/restore/", methods=["GET"])
def restore_all_from_JSON():
    result = load_episodes_JSON_backup()
    return jsonify({'result': result})



if __name__ == "__main__":

    episodes.execute_sql()
    tasks.execute_sql()

    app.run(debug=True)