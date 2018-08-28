# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import os


class Config(object):
    DEBUG = False


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class Test(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    DEBUG = True
    DEVELOPMENT = True


class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DEBUG = False
