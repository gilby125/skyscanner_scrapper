# coding: utf-8


from datetime import datetime

from flask import jsonify
from flask.views import MethodView


class HealthAPI(MethodView):
    def get(self):
        # We should add some real world checks to this. Let's leave it like this for now
        health = {
            "health": "ok",
            "timestamp": datetime.isoformat(datetime.utcnow()),
        }
        return jsonify(health)
