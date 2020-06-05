#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="mapaguarani",
    version="0.1",
    author="Bruno Martin",
    author_email="bruno@hacklab.com.br",
    packages=[
        "mapaguarani",
    ],
    include_package_data=True,
    install_requires=[
        "Django==1.11.29",
    ],
    zip_safe=False,
    scripts=["mapaguarani/manage.py"],
)
