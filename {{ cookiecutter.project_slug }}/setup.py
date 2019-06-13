#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='{{ cookiecutter.package_slug }}',
    version="0.1.0",
    description='{{ cookiecutter.participant_name }}',
    author='{{ cookiecutter.author_name }}',
    author_email='{{ cookiecutter.author_email }}',
    install_requires=[
        'polyswarm-artifact',
        'polyswarm-client'
    ],
    include_package_data=True,
    packages=['{{ cookiecutter.package_slug }}'],
    package_dir={
        '{{ cookiecutter.package_slug }}': '{{ cookiecutter.package_slug }}',
    },
)
