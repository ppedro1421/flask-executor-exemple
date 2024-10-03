from flask import Blueprint, current_app, request, jsonify
from app import executor
from app.tasks import background_task

bp = Blueprint("main", __name__)


@bp.route('/')
def index():
    current_app.logger.debug("Hello World!")
    return "Hello World!"


@bp.route('/start-task')
def start_task():
    data = request.get_json()
    task_id = data.get('task_id')

    current_app.logger.info("start-task %s", task_id)

    executor.submit_stored(task_id, background_task, task_id)
    return jsonify({'result': 'success', 'id': task_id})


@bp.route('/get-result')
def get_result():
    data = request.get_json()
    task_id = data.get('task_id')

    current_app.logger.info("get-task-status %s", task_id)

    if not executor.futures.done(task_id):
        return jsonify({'status': executor.futures._state(task_id)})

    future = executor.futures.pop(task_id)
    return jsonify({'status': 'DONE', 'result': future.result()})
