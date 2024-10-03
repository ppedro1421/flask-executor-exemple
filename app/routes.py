from flask import Blueprint, current_app, request, jsonify
from app import executor
from app.tasks import background_task

bp = Blueprint("main", __name__)


@bp.route('/', methods=['GET'])
def index():
    current_app.logger.debug("Hello World!")
    return "Hello World!"


@bp.route('/task-start', methods=['POST'])
def start_task():
    data = request.get_json()
    task_id = data.get('task_id')

    current_app.logger.info("task start %s", task_id)

    executor.submit_stored(task_id, background_task, task_id)
    return jsonify({'result': 'success', 'id': task_id})


@bp.route('/task-result', methods=['POST'])
def get_result():
    data = request.get_json()
    task_id = data.get('task_id')

    current_app.logger.info("task result %s", task_id)

    if not executor.futures.done(task_id):
        return jsonify({'status': executor.futures._state(task_id)})

    future = executor.futures.pop(task_id)
    return jsonify({'status': 'DONE', 'result': future.result()})


@bp.route('/stress-test', methods=['POST'])
def stress_test():
    current_app.logger.info("start stress test")

    executor.submit(background_task, 1)
    executor.submit(background_task, 2)
    executor.submit(background_task, 3)
    executor.submit(background_task, 4)
    executor.submit(background_task, 5)
    executor.submit(background_task, 6)
    executor.submit(background_task, 7)
    executor.submit(background_task, 8)
    executor.submit(background_task, 9)

    return jsonify({'result': 'success'})
