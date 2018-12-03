#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import unittest

from malwarerepoclient.client import DummyMalwareRepoClient
from {{ cookiecutter.package_slug }} import Microengine, Scanner


class TestEicar{{ cookiecutter.engine_name_slug|capitalize }}(unittest.TestCase):
    micro_engine_cls = Microengine
    malware_repo_client_cls = DummyMalwareRepoClient

    def test_scan_random_mal_not(self):
        me = Scanner()
        {% if cookiecutter.has_backend == "true" %}
        me.wait_for_backend()
        {% endif %}
        for t in [True, False]:
            mal_md, mal_content = self.malware_repo_client_cls().get_random_file(malicious_filter=t)

            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)

            async def run_t():
                bit, infected, infected_str = await me.scan("nocare", mal_content, "home")

                self.assertEqual(infected, t)

            coro = asyncio.coroutine(run_t)
            event_loop.run_until_complete(coro())
            event_loop.close()
