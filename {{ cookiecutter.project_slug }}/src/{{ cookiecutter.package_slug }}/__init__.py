#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
import logging
import os

from polyswarmclient.abstractmicroengine import AbstractMicroengine
from polyswarmclient.abstractscanner import AbstractScanner, ScanResult

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
    async def wait_for_backend(self):
        # CUSTOMIZE_HERE
        # If you scanner has a disjoint backend, you'll want to properly detect when that backend is available.
        raise NotImplementedError
    {% endif %}
    async def scan(self, guid, content, chain):
        """
        Args:
            guid (str): GUID of the bounty under analysis, use to track artifacts in the same bounty
            content (bytes): Content of the artifact to be scan
            chain (str): Chain we are operating on
        Returns:
            ScanResult: Result of this scan
        """
        # CUSTOMIZE_HERE
        # This is where you implement your scanner's logic.
        raise NotImplementedError


class Microengine(AbstractMicroengine):
    """
        {{ cookiecutter.engine_name }}
    """

    def __init__(self, client, testing=0, scanner=None, chains=None):
        """
        Initialize {{ cookiecutter.engine_name }}

        Args:
            client ('Client'): Client to use
            testing (int): How many test bounties to respond to (shutdown once this is reached) (0 is no limit)
            scanner ('Scanner'): Scanner we are using to process artifacts
            chains (set[str]): Chain we are operating on
        """
        logger.info("Loading {{ cookiecutter.engine_name }} scanner...")
        scanner = Scanner()
        {% if cookiecutter.has_backend == "true" %}
        client.on_run.register(self.handle_run)
        {% endif %}
        super().__init__(client, testing, scanner, chains)
    {% if cookiecutter.has_backend == "true" %}
    async def handle_run(self, chain):
        """
        Often you'll want to use asyncio code in your wait_for_backend() method.
        Thus, you need to ensure it is called AFTER the asyncio loop starts.
        Registering this method with client.on_run.register() ensures it is called immediately when the loop starts.

        :param chain:
        :return:
        """
        await self.scanner.wait_for_backend()
    {% endif %}
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
