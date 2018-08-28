# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

from extensions import db


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    register_blueprints(app)
    register_extensions(app)

    return app

def register_extensions(app):
    db.init_app(app)

def register_blueprints(app):
    # Import and register blueprints here.
    from doctor_service.api import doctor_api, appointment_api

    app.register_blueprint(doctor_api.doctor_api)
    app.register_blueprint(appointment_api.appointment_api)
