{% if cookiecutter.participant_type == "microengine" -%}
from .{{cookiecutter.participant_name_slug}} import Scanner
{% elif cookiecutter.participant_type == "ambassador" -%}
from .{{cookiecutter.participant_name_slug}} import Ambassador
{%endif-%}

__version__ = "0.1.0"
