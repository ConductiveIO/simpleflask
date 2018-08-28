# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from setuptools import find_packages, setup

from version import VERSION

__author__ = ""


def read_from_req(f_name="requirements.txt"):
    ret = []
    with open(f_name) as f:
        for line in f:
            line = line.strip()
            if line.startswith('-') or line.startswith('#'):
                # This is a comment or index url, ignore it
                pass
            elif line:
                ret.append(line)
    return ret


requires = read_from_req()

setup(name="user-service",
      version=VERSION,
      description="user-service",
      packages=find_packages(),
      install_requires=requires,
      entry_points={
      },
      include_package_data=True
      )
