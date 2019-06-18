#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

logger = logging.getLogger(__name__)  # Init logger

{% if cookiecutter.participant_type == "microengine" -%}

from polyswarmclient.abstractmicroengine import AbstractMicroengine
from polyswarmclient.abstractscanner import AbstractScanner, ScanResult
from polyswarmartifact import ArtifactType

# CUSTOMIZE_HERE
# If your engine must call out to a scan engine binary, customize this path to match the location of that backend, e.g.:
# PATH_SCANNER_BINARY = os.getenv(
#     "PS_PATH_SCANNER_BINARY",
#     os.path.join(
#         os.path.dirname(__file__),
#         "..",
#         "..",
#         "pkg",
#         {% if cookiecutter.platform == "linux" %}"{{ cookiecutter.participant_name_slug }}.sh"){% endif %}
#         {% if cookiecutter.platform == "windows" %}"{{ cookiecutter.participant_name_slug }}.exe"){% endif %}
#     )


class Scanner(AbstractScanner):

    def __init__(self):
        super(Scanner, self).__init__()

    async def scan(self, guid, artifact_type, content, chain):
        """
        Args:
            guid (str): GUID of the bounty under analysis, use to track artifacts in the same bounty
            artifact_type (ArtifactType): Artifact type for the bounty
            content (bytes): Content of the artifact to be scan
            chain (str): Chain we are operating on
        Returns:
            ScanResult: Result of this scan
        """
        # CUSTOMIZE_HERE
        # This is where you implement your scanner's logic.
        raise NotImplementedError

    async def setup(self):
        """Override this method to implement custom setup logic.
        This is run by arbiters, microengines, and workers after the Scanner class is instantiated and before any calls to the scan() method.
        Args:

        Returns:
            status (bool): Did setup complete successfully?
        """
        # CUSTOMIZE_HERE
        # If your participant requires time to, e.g. connect to an external service before it can process requests,
        # check for the availability of the service here. Return True when ready, False if there's an error.
        return True

{% endif -%}

{% if cookiecutter.participant_type == "ambassador" -%}

from polyswarmclient.abstractambassador import AbstractAmbassador

BOUNTY_TEST_DURATION_BLOCKS = int(os.getenv('BOUNTY_TEST_DURATION_BLOCKS', 5))


class Ambassador(AbstractAmbassador):
    """
        {{ cookiecutter.participant_name }}
    """

    def __init__(self, client, testing=0, chains=None, watchdog=0, submission_rate=30):
        """
        Initialize {{ cookiecutter.participant_name }}

        Args:
            client (`Client`): Client to use
            testing (int): How many test bounties to respond to
            chains (set[str]): Chain(s) to operate on
            watchdog: interval over which a watchdog thread should verify bounty placement on-chain (in number of blocks)
            submission_rate: if nonzero, produce a sleep in the main event loop to prevent the ambassador from overloading `polyswarmd` during testing
        """
        super().__init__(client, testing, chains, watchdog, submission_rate)

    async def generate_bounties(self, chain):
        """
        Initialize {{ cookiecutter.participant_name }}

        Args:
            chain (str): Chain sample is being requested from
        """
        # CUSTOMIZE_HERE
        # This is where you implement your ambassador's bounty generation logic.
        raise NotImplementedError

{% endif -%}
