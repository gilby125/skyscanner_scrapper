# coding: utf-8

from flask import Blueprint
from .views import HealthAPI


blueprint = Blueprint("health", __name__)

health_view_func = HealthAPI.as_view("health")
blueprint.add_url_rule("", view_func=health_view_func)
blueprint.add_url_rule("/", view_func=health_view_func)
