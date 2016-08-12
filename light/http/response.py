import json

from flask import Response
from light.mongo.encoder import JsonEncoder


def send(data, error=None):
    result = {
        'apiVersion': '1.0', 'data': data
    }

    if error:
        result = {
            'apiVersion': '1.0',
            'error': {
                'code': error.code,
                'message': error.message,
                'errors': data
            }
        }

    return Response(
        json.dumps(result, cls=JsonEncoder),
        mimetype='application/json; charset=UTF-8',
        status=200
    )
