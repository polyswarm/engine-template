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
    remove_directory("packer")
    remove_file("template.json")
    remove_file("microengine_keyfile")


# def remove_linux_content():
#     remove_directory("docker")
#     remove_file(".dockerignore")


if __name__ == '__main__':

    if platform == "linux":
        # remove windows specific folders/files
        remove_windows_content()

    # if platform == "windows":
    #     # remove linux specific folders/files
    #     remove_linux_content()
