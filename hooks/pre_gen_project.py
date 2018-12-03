#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

platform = '{{ cookiecutter.platform }}'
engine_name_slug = '{{ cookiecutter.engine_name_slug }}'
author_org_slug = '{{ cookiecutter.author_org_slug }}'
has_backend = '{{ cookiecutter.has_backend }}'


if platform not in ["windows", "docker-linux"]:
    print("ERROR {} is not a valid platform".format(platform))
    sys.exit(1)

for ic in ["_", " ", "-", "."]:
    if ic in engine_name_slug:
        print("ERROR {} must not exist in engine name slug".format(ic))
        sys.exit(1)

for ic in ["_", " ", "-", "."]:
    if ic in author_org_slug:
        print("ERROR {} must not exist in author org slug".format(ic))
        sys.exit(1)

if has_backend not in ["false", "true"]:
    print("ERROR {} is not a valid option for has_backend".format(has_backend))
    sys.exit(1)
