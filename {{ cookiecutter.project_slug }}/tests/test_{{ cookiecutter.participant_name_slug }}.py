#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import pytest

{% if cookiecutter.participant_type == "microengine" %}

import sys
from malwarerepoclient.client import DummyMalwareRepoClient
from {{ cookiecutter.package_slug }} import Microengine, Scanner
from polyswarmartifact import ArtifactType

{% endif %}

{% if cookiecutter.participant_type == "ambassador" %}

from {{ cookiecutter.package_slug }} import Ambassador

{% endif %}

{% if cookiecutter.participant_type == "microengine" %}

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
    await scanner.setup()

    for t in [True, False]:
        mal_md, mal_content = DummyMalwareRepoClient().get_random_file(malicious_filter=t)
        result = await scanner.scan("nocare", ArtifactType.FILE, mal_content, "home")
        assert result.verdict == t

{% endif %}

{% if cookiecutter.participant_type == "ambassador" %}

# TODO: implement unit tests for ambassadors

@pytest.mark.asyncio
async def todo():
    """
    TODO
    """
    assert True is True

{% endif %}
