#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

participant_type = '{{ cookiecutter.participant_type }}'
platform = '{{ cookiecutter.platform }}'

participant_name_slug = '{{ cookiecutter.participant_name_slug }}'

author_org_slug = '{{ cookiecutter.author_org_slug }}'

# Microengines only
microengine__has_backend = '{{ cookiecutter.microengine__has_backend }}'

if participant_type not in ["microengine", "ambassador"]:
    print("ERROR {} is not a valid participant type".format(participant_type))
    sys.exit(1)

if platform not in ["windows", "linux"]:
    print("ERROR {} is not a valid platform".format(platform))
    sys.exit(1)

for ic in ["_", " ", "-", "."]:
    if ic in participant_name_slug:
        print("ERROR {} must not exist in engine name slug".format(ic))
        sys.exit(1)

for ic in ["_", " ", "-", "."]:
    if ic in author_org_slug:
        print("ERROR {} must not exist in author org slug".format(ic))
        sys.exit(1)

# Microengines only
if participant_type == "microengine":

    if microengine__has_backend not in ["false", "true"]:
        print("ERROR {} is not a valid option for microengine__has_backend".format(microengine__has_backend))
        sys.exit(1)
