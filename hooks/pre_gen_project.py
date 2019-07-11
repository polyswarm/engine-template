#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

participant_type = '{{ cookiecutter.participant_type }}'
platform = '{{ cookiecutter.platform }}'

participant_name_slug = '{{ cookiecutter.participant_name_slug }}'

author_org_slug = '{{ cookiecutter.author_org_slug }}'

if participant_type not in ["microengine", "ambassador", "arbiter"]:
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

# Only Microengines are supported on Windows
if platform == "windows" and participant_type != "microengine":
    print("ERROR: {} are not supported on Windows. ".format(participant_type))
    sys.exit(1)
