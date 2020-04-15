import uuid
from typing import Any
from flask import Flask, abort, jsonify, request
from rq import Queue
from image_resizer.compress_image import task_run
from image_resizer.config import redis_conn

app = Flask(__name__)
queue = Queue(connection=redis_conn)


@app.route('/task', methods=['POST'])
def new_task() -> Any:
    if not request.json or 'image' not in request.json:
        abort(400)
    image = request.json['image']
    image_id = str(uuid.uuid1())
    job = queue.enqueue(task_run, image_id, image)
    return jsonify({'image_id': image_id, 'job_id': job.id, 'status': 'in process'}), 200


@app.route('/task/<string:tasks_id>', methods=['GET'])
def get_tasks_status(tasks_id: str) -> Any:
    job = queue.fetch_job(tasks_id)
    if not job:
        return jsonify({'error': 'Not found'}), 404

    if job.is_finished:
        return jsonify({'status': 'done', 'images_id': 'lol'}), 200
    else:
        return jsonify({'status': 'in process', 'images_id': 'lol'}), 200


@app.route('/image/<string:images_id>', methods=['GET'])
def get_image(images_id: str) -> Any:
    if (
        not request.json
        or 'size' not in request.args
    ):
        abort(400)
    size = request.args.get('size')
    image = redis_conn.get(f'{images_id}_{size}')
    return jsonify({'image': image}), 200


if __name__ == '__main__':
    app.run()
