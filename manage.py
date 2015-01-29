#!/usr/bin/env python
# coding: utf-8


import sys

from flask.ext.script import Manager

from scrapper import create_app


app = create_app("scrapper.config.local")
manager = Manager(app)


@manager.command
def test():
    print >>sys.stderr, "This option is deprecated. Use nosetests instead."
    sys.exit(1)


@manager.command
def lint():
    print "PyLint Report"
    print "============="
    from pylint.lint import Run
    Run(['--rcfile=pylintrc', 'scrapper'], exit=False)

    print "Flake8 Report"
    print "============="
    from flake8.engine import get_style_guide
    flake8_style = get_style_guide(config_file="flake8.cfg", parse_argv=False, paths=["scrapper"])
    flake8_style.check_files()

if __name__ == '__main__':
    manager.run()