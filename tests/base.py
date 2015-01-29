# coding: utf-8

import os
from flask.ext.testing import TestCase
from scrapper import create_app

class BaseTestCase(TestCase):
    def create_app(self):
        os.environ["SCRAPPER_SETTINGS"] = "tests.settings"
        return create_app("tests.settings")
