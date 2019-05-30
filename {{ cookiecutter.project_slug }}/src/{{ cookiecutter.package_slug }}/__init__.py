#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import os

logger = logging.getLogger(__name__)  # Init logger

{% if cookiecutter.participant_type == "microengine" %}

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

    { % if cookiecutter.microengine__has_backend == "true" %}
    async def setup(self):
        """Override this method to implement custom setup logic.
        This is run by arbiters, microengines, and workers after the Scanner class is instantiated and before any calls to the scan() method.
        Args:

        Returns:
            status (bool): Did setup complete successfully?
        """
        return True

    { % endif %}


class Microengine(AbstractMicroengine):
    """
        {{ cookiecutter.participant_name }}
    """

    def __init__(self, client, testing=0, scanner=None, chains=None, artifact_types=None):
        """
        Initialize {{ cookiecutter.participant_name }}

        Args:
            client ('Client'): Client to use
            testing (int): How many test bounties to respond to (shutdown once this is reached) (0 is no limit)
            scanner ('Scanner'): Scanner we are using to process artifacts
            chains (set[str]): Chain we are operating on
            artifact_types (list[ArtifactType]): List of artifact types this can scan
        """
        logger.info("Loading {{ cookiecutter.participant_name }} scanner...")
        if artifact_types is None:
            artifact_types = [ArtifactType.FILE, ArtifactType.URL]
        scanner = Scanner()
        super().__init__(client, testing, scanner, chains, artifact_types)

    async def bid(self, guid, mask, verdicts, confidences, metadatas, chain):
        """
        Args:
            guid (str): GUID of the bounty under analysis, use to correlate with artifacts in the same bounty
            masks (list[bool]): mask for the from scanning the bounty files
            verdicts (list[bool]): scan verdicts from scanning the bounty files
            confidences (list[float]): Measure of confidence of verdict per artifact ranging from 0.0 to 1.0
            metadatas (list[str]): metadata blurbs from scanning the bounty files
            chain (str): Chain we are operating on
        Returns:
            (int): Amount of NCT to bid in base NCT units (10 ^ -18)
        """
        # CUSTOMIZE_HERE
        # You'll want to drop in your own bid amount logic here.
        # Default logic is to always place the minimum bid amount.
        return await self.client.bounties.parameters[chain].get('assertion_bid_minimum')
{% endif %}

{% if cookiecutter.participant_type == "ambassador" %}

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

{% endif %}
