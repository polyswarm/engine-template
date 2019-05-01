{% if cookiecutter.platform == "windows" %}# escape=`
FROM polyswarm/polyswarm-client-windows:latest

COPY . C:\microengine\
WORKDIR C:\microengine\

RUN pip install --no-warn-script-location -r requirements.txt .

# RUN Install-Service -Name microengine -Path C:\Python36\Scripts\microengine.exe
# RUN Install-Service -Name worker -Path C:\Python36\Scripts\worker.exe

CMD powershell

{% endif %}






{% if cookiecutter.platform == "linux" %}

FROM polyswarm/polyswarm-client

# remove polyswarm client source, since it was already installed, but keep testing keyfiles
RUN mv /usr/src/app /usr/src/psc \
 && mkdir -p /usr/src/app/docker \
 && cp -a /usr/src/psc/docker/*_keyfile /usr/src/app/docker/ \
 && rm -rf /usr/src/psc

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y unzip

COPY . .

{% if cookiecutter.participant_type == "microengine" %}
# CUSTOMIZE_HERE
# This is where you would copy you scanner backend binary into the Docker image, e.g.:
# COPY myscanner.bin .
{% endif %}

RUN set -x && pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .

CMD ["{{ cookiecutter.participant_type }}", "--backend", "{{ cookiecutter.author_org_slug }}_{{ cookiecutter.participant_name_slug }}"]

{% endif %}
