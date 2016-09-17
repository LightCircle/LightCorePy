import json

from werkzeug.wsgi import wrap_file
from light.mongo.encoder import JsonEncoder


def send(handler, data, error=None):
    # return error
    if error is not None:
        return send_error(handler, data, error)

    if data is None:
        data = {}

    # return json
    if isinstance(data, dict):
        return send_json(handler, data)

    # return file
    return send_file(handler, data)


def send_file(handler, data):
    if handler.res.headers.get('Content-type') == 'text/html; charset=utf-8':
        handler.res.headers.get('Content-type', 'application/octet-stream')

    handler.res.response = wrap_file(handler.req.environ, data)
    return handler.res


def send_json(handler, data):
    result = {
        'apiVersion': '1.0', 'data': data
    }

    handler.res.data = json.dumps(result, cls=JsonEncoder)
    handler.res.mimetype = 'application/json; charset=utf-8'
    handler.res.status_code = 200

    return handler.res


def send_error(handler, data, error=None):
    result = {
        'apiVersion': '1.0',
        'error': {
            'code': error.code,
            'message': error.message,
            'errors': data
        }
    }

    handler.res.data = json.dumps(result, cls=JsonEncoder)
    handler.res.mimetype = 'application/json; charset=utf-8'
    handler.res.status_code = error.code

    return handler.res
