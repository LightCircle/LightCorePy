import json

from datetime import datetime
from bson import ObjectId


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        return json.JSONEncoder.default(self, obj)
