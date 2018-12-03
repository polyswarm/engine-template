#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='{{ cookiecutter.package_slug }}',
    version='0.1',
    description='A basic microengine development framework',
    author='{{ cookiecutter.author_name }}',
    author_email='{{ cookiecutter.author_email }}',
    include_package_data=True,
    packages=['{{ cookiecutter.package_slug }}'],
    package_dir={
        '{{ cookiecutter.package_slug }}': 'src/{{ cookiecutter.package_slug }}',
    },
)
