#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

from polyswarmartifact import ArtifactType
from polyswarmartifact.schema.verdict import Verdict

{% if cookiecutter.participant_type == "microengine" or 
      cookiecutter.participant_type == "arbiter" -%}

from polyswarmclient.abstractscanner import AbstractScanner, ScanResult
{% endif -%}

{% if cookiecutter.participant_type == "microengine" -%}
from polyswarmclient.bidstrategy import BidStrategyBase

import {{ cookiecutter.package_slug }}

{% endif -%}

{% if cookiecutter.participant_type == "microengine" or 
      cookiecutter.participant_type == "arbiter" -%}

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

{% if cookiecutter.participant_type == "microengine" -%}

logger = logging.getLogger(__name__)  # Init logger

class BidStrategy(BidStrategyBase):
    """
    Microengine developers may subclass BidStrategyBase to modify default bid logic paramters or implement fully custom bidding (staking) logic.

    BidStrategyBase's default bid() strategy:
    1. averages confidences over all artifacts in the given bounty, arriving at a single value
    2. fits this value on a bid scale, the boundaries of which are set via minimum and maximum multipliers supplied via its constructor

    View the code: https://github.com/polyswarm/polyswarm-client/blob/master/src/polyswarmclient/bidstrategy.py

    NOTE: Assertions for multi-artifact bounties only permit a single bid amount.
    This is a known limitation that will be removed in the near future.
    Soon, a mapping of N bids to N artifacts in a single assertion will be supported.
    Once this is supported, the default bif strategy of producing an average bid across all bounties will be deprecated.
    """

    # CUSTOMIZE BELOW

    # Override BidStrategyBase's:
    # * constructor: to alter the minimum & maximum bid multipliers used in the default bid method
    def __init__(self):
        """
        The absolute minimum bid amount is currently 0.0625 NCT.

        With a min_bid_multiplier of:
        * 8: the floor is set to 0.5 NCT (0.0625 * 8)

        With a max_bid_multiplier:
        * 8: the ceiling is set to 0.5 NCT (0.0625 * 8)

        If min_bid_multiplier < max_bid_multiplier, the floor and ceiling differ.
        Confidence is used to determine where the bid falls in the range.
        """
        super().__init__(min_bid_multiplier=8, max_bid_multiplier=8)

    # Override BidStrategyBase's:
    # * bid() method: to implement fully custom bid logic
    #def bid(self):
        # my custom bid logic

{% endif -%}

class {{ cookiecutter.participant_name_slug|title }}:
    """
    CUSTOMIZE_HERE
        This is where you implement your scanner's logic.
    """
    def __init__(self):
        pass

    async def setup(self):
        """
        Override this method to implement custom setup logic.

        Returns:
            status (bool): Did setup complete successfully?
        """

        # CUSTOMIZE_HERE
        # If your participant requires time to, e.g. connect to an external service before it can process requests,
        # check for the availability of the service here. Return True when ready, False if there's an error.
        return True

    async def file_scan(self, content, metadata):
        """
        Implement your File Scan microengine

        Args:
            content (bytes): binary content
            metadata (object): metadata object

        Returns: 
            ScanResult: Result of this scan
        """

        # ScanResult Object: 
        #
        # bit : a boolean representing a malicious or benign determination
        # verdict: another boolean representing whether the engine wishes to assert on the artifact
        # metadata: an object describing our scan results

        # return ScanResult(bit=bit_variable, 
        #                   verdict=verdict_variable,
        #                   metadata=metadata.json())

        raise NotImplementedError

    async def url_scan(self, content, metadata):
        """
        Implement your URL Scan microengine
        
        Args:
            content (bytes): binary content
            metadata (object): metadata object

        Returns: 
            ScanResult: Result of this scan
        """

        # ScanResult Object: 
        #
        # bit : a boolean representing a malicious or benign determination
        # verdict: another boolean representing whether the engine wishes to assert on the artifact
        # metadata: an object describing our scan results

        # return ScanResult(bit=bit_variable, 
        #                   verdict=verdict_variable,
        #                   metadata=metadata.json())

        raise NotImplementedError


class Scanner(AbstractScanner):

    def __init__(self):
        super(Scanner, self).__init__()
        self.{{ cookiecutter.participant_name_slug }} = {{cookiecutter.participant_name_slug|title}}()

    async def setup(self):
        """
        Override this method to implement custom setup logic.
        This is run by arbiters and microengines after the Scanner class is instantiated and before any calls to the scan() method.

        Returns:
            status (bool): Did setup complete successfully?
        """
        return await self.{{ cookiecutter.participant_name_slug }}.setup()

    async def scan(self, guid, artifact_type, content, metadata, chain):
        """
        Args:
            guid (str): GUID of the bounty under analysis, use to track artifacts in the same bounty
            artifact_type (ArtifactType): Artifact type for the bounty
            content (bytes): Content of the artifact to be scan
            chain (str): Chain we are operating on
        Returns:
            ScanResult: Result of this scan
        """
        metadata = Verdict().set_malware_family('')\
                            .set_scanner(operating_system=platform.system(),
                                         architecture=platform.machine(),
                                         vendor_version='',
                                         version={{ cookiecutter.package_slug }}.__version__)

        # Binary File Scan
        if artifact_type == ArtifactType.FILE:
            return await self.{{ cookiecutter.participant_name_slug }}.file_scan(content, metadata)
        # URL Scan
        elif artifact_type == ArtifactType.URL:
            return await self.{{ cookiecutter.participant_name_slug }}.url_scan(content, metadata)
        # Not supported artifact
        else:
            logger.error('Invalid artifact_type. Skipping bounty.')
            return ScanResult(metadata=metadata.json())
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
