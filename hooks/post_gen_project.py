#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

platform = '{{ cookiecutter.platform }}'


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_directory(dirpath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, dirpath))


def remove_windows_content():
    remove_file("microengine_keyfile")


if __name__ == '__main__':

    if platform == "linux":
        remove_windows_content()
