# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import os

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

import doctor_service.settings as settings
from doctor_service.app import create_app
from doctor_service.extensions import db

app = create_app(settings.Development)

from doctor_service.models import Doctor, Location, Appointment

app.config.from_object(settings.Development)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('runserver', Server(threaded=True))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import subprocess
    command = 'nosetests --with-xunit --with-coverage --cover-package=doctor_service --cover-erase'.split(' ')
    subprocess.call(command)

if __name__ == "__main__":
    manager.run()
