# coding: utf-8

from flask import Blueprint
from .views import Scrapper


blueprint = Blueprint("scrapper", __name__, template_folder="templates", static_folder="static")

scrapper_view_func = Scrapper.as_view("scrapper")
blueprint.add_url_rule("", view_func=scrapper_view_func)
