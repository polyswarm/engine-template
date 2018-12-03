#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
import logging
import os

from polyswarmclient.abstractmicroengine import AbstractMicroengine
from polyswarmclient.abstractscanner import AbstractScanner

logger = logging.getLogger(__name__)  # Init logger

# todo: update the path to your scanner binary
PATH_SCANNER_BINARY = os.getenv(
    "PS_PATH_SCANNER_BINARY",
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "pkg",
        "{{ cookiecutter.engine_name_slug|capitalize }}.exe")
    )


class Scanner(AbstractScanner):

    def __init__(self):
        super(Scanner, self).__init__()
    {% if cookiecutter.has_backend == "true" %}
    def wait_for_backend(self):
        import time
        time.sleep(10)
        # todo replace me with something more intelligent
    {% endif %}
    async def scan(self, guid, content, chain):
        """
        :param guid:
        :param content:
        :param chain:
        :return:
        """
        pass


class Microengine(AbstractMicroengine):
    """
        {{ cookiecutter.engine_name|capitalize }}Microengine
    """

    def __init__(self, client, testing=0, scanner=None, chains={'side'}):
        """
        Initialize {{cookiecutter.engine_name|capitalize}}

        :param client:
        :param testing:
        :param scanner:
        :param chains:
        """
        logger.info("Loading {{cookiecutter.engine_name|capitalize}} scanner...")
        scanner = Scanner()
        # todo is this the right place to wait for backend to be up?
        {% if cookiecutter.has_backend == "true" %}
        scanner.wait_for_backend()
        {% endif %}
        super().__init__(client, testing, scanner, chains)
