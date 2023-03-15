import os
import uuid

import flask
from flask import Flask
from flask.views import MethodView
from flask import jsonify
from flask import request

from celery import Celery
from celery.result import AsyncResult

from upscale import upscale

app_name = 'app'
app = Flask(app_name)
app.config['UPLOAD_FOLDER'] = 'files'

celery = Celery(app_name, broker='redis://127.0.0.1:6379/1', backend='redis://127.0.0.1:6379/2')
celery.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


@celery.task
def upscale_image(path, extension):
    new_path = os.path.join('files', f'{uuid.uuid4()}.{extension}')
    upscale(path, new_path)
    return new_path


class UpScaleMethods(MethodView):

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({'status': task.status,
                        'file_link': task.result})

    def post(self):
        image = request.files.get('image')
        extension = image.filename.split('.')[-1]
        path = os.path.join('files', f'{uuid.uuid4()}.{extension}')
        image.save(path)

        task = upscale_image.delay(path, extension)
        return jsonify(
            {'task_id': task.id})


def get_file(file_link):
    try:
        return flask.send_file(file_link, as_attachment=True)
    except FileNotFoundError:
        http_response = jsonify({'status': 'File not found'})
        http_response.status_code = 404
        return http_response


upscale_view = UpScaleMethods.as_view('upscalemethods')
app.add_url_rule('/upscale/', view_func=upscale_view, methods=['POST'])
app.add_url_rule('/tasks/<string:task_id>', view_func=upscale_view, methods=['GET'])
app.add_url_rule('/processed/<string:file_link>', view_func=get_file, methods=['GET'])


if __name__ == '__main__':
    app.run()
