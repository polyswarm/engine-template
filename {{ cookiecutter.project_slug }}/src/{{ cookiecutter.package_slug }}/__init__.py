#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
import logging
import os

from polyswarmclient.abstractmicroengine import AbstractMicroengine
from polyswarmclient.abstractscanner import AbstractScanner

logger = logging.getLogger(__name__)  # Init logger

# CUSTOMIZE_HERE
# If your engine must call out to a scan engine binary, customize this path to match the location of that backend, e.g.:
# PATH_SCANNER_BINARY = os.getenv(
#     "PS_PATH_SCANNER_BINARY",
#     os.path.join(
#         os.path.dirname(__file__),
#         "..",
#         "..",
#         "pkg",
#         {% if cookiecutter.platform == "docker-linux" %}"{{ cookiecutter.engine_name_slug }}.sh"){% endif %}
#         {% if cookiecutter.platform == "windows" %}"{{ cookiecutter.engine_name_slug }}.exe"){% endif %}
#     )


class Scanner(AbstractScanner):

    def __init__(self):
        super(Scanner, self).__init__()
    {% if cookiecutter.has_backend == "true" %}
    def wait_for_backend(self):
        # CUSTOMIZE_HERE
        # If you scanner has a disjoint backend, you'll want to properly detect when that backend is available.
        raise NotImplementedError
    {% endif %}
    async def scan(self, guid, content, chain):
        """
        Args:
            guid (str): GUID of the bounty under analysis, use to track artifacts in the same bounty
            content (bytes): Content of the artifact to be scan
        Returns:
            Tuple(bool, bool, str): Tuple of bit, verdict, metadata

        Note:
            | The meaning of the return types are as follows:
            |   - **bit** (*bool*): Whether to include this artifact in the assertion or not
            |   - **verdict** (*bool*): Whether this artifact is malicious or not
            |   - **metadata** (*str*): Optional metadata about this artifact
        """
        # CUSTOMIZE_HERE
        # This is where you implement your scanner's logic.
        raise NotImplementedError


class Microengine(AbstractMicroengine):
    """
        {{ cookiecutter.engine_name }}
    """

    def __init__(self, client, testing=0, scanner=None, chains={'side'}):
        """
        Initialize {{ cookiecutter.engine_name }}

        :param client:
        :param testing:
        :param scanner:
        :param chains:
        """
        logger.info("Loading {{ cookiecutter.engine_name }} scanner...")
        scanner = Scanner()
        {% if cookiecutter.has_backend == "true" %}
        scanner.wait_for_backend()
        {% endif %}
        super().__init__(client, testing, scanner, chains)

    def bid(self, guid, chain):
        """
        Args:
            guid (str): GUID of the bounty under analysis, use to correlate with artifacts in the same bounty
            chain (str): Chain we are operating on
        Returns:
            (int): Amount of NCT to bid in base NCT units (10 ^ -18)
        """
        # CUSTOMIZE_HERE
        # You'll want to drop in your own bid amount logic here.
        # Default logic is to always place the minimum bid amount.
        return self.client.bounties.parameters[chain]['assertion_bid_minimum']
