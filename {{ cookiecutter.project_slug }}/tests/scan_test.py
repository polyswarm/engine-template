#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import pytest
import sys

from malwarerepoclient.client import DummyMalwareRepoClient
from {{ cookiecutter.package_slug }} import Microengine, Scanner


@pytest.yield_fixture()
def event_loop():
    """
    To enable Windows engines to support subprocesses in asyncio, they need to use the ProactorEventLoop.

    When the engine is running via polyswarm-client, this is handled by polyswarm-client.
    But when using pytest, you do not run the engine via polyswarm-client, so you have to change the loop in a fixture.

    ref: https://docs.python.org/3/library/asyncio-eventloops.html

    :return: event loop object
    """
    loop = asyncio.get_event_loop()
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_scan_random_mal_not():
    """
    Run scanner against one malicious file (EICAR) and one non-malicious file.

    """
    scanner = Scanner()
    {% if cookiecutter.has_backend == "true" %}
    scanner.wait_for_backend()
    {% endif %}

    for t in [True, False]:
        mal_md, mal_content = DummyMalwareRepoClient().get_random_file(malicious_filter=t)
        bit, is_infected, infected_str = await scanner.scan("nocare", mal_content, "home")
        assert is_infected == t
