# coding: utf-8

import os
import logging
import logging.handlers
from flask import Flask

ROOTDIR = os.path.dirname(os.path.dirname(__file__))


def get_conf(settings):
    settings = os.environ.get("SCRAPPER_SETTINGS", settings)

    if not settings:
        raise RuntimeError("SCAPPER_SETTINGS environment variable must be defined.")

    return settings


def create_app(settings=None):
    app = Flask(__name__)
    app.config.from_object(get_conf(settings))

    # blueprints
    from .scrapper_blueprint.blueprint import blueprint as scrapper
    from .health.blueprint import blueprint as health

    app.register_blueprint(scrapper, url_prefix='/')
    app.register_blueprint(health, url_prefix="/health")

    if app.config.get("REQUEST_LOG", False):
        logfile = os.path.join(ROOTDIR, 'logs', 'scrapper.log')

        handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=5*1024*1024, backupCount=5)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)s: %(message)s"))

        app.logger.addHandler(handler)
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.ERROR)

    return app
