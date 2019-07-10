{% if cookiecutter.platform == "windows" -%}# escape=`
FROM polyswarm/polyswarm-client-windows:latest

WORKDIR C:\microengine\

# -- Install Prerequisites -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -- Copy & Install Participant ------------------------
COPY . .
RUN python setup.py install

CMD ["powershell"]

{% endif -%}

{% if cookiecutter.platform == "linux" -%}

FROM polyswarm/polyswarm-client:latest

# -- Remove polyswarm-client Source from Base Image ----
RUN mv /usr/src/app /usr/src/psc \
 && mkdir -p /usr/src/app/docker \
 && cp -a /usr/src/psc/docker/*_keyfile /usr/src/app/docker/ \
 && rm -rf /usr/src/psc

WORKDIR /usr/src/app

# -- Install Prerequisites -----------------------------
COPY requirements.txt .
RUN set -x && pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y unzip

{% if cookiecutter.participant_type == "microengine" -%}
# CUSTOMIZE_HERE
# This is where you would copy you scanner backend binary into the Docker image, e.g.:
# COPY myscanner.bin .
{% endif -%}

# -- Copy & Install Participant ------------------------
COPY . .
RUN pip install --no-cache-dir .

CMD ["{{ cookiecutter.participant_type }}", "--backend", "{{ cookiecutter.author_org_slug }}_{{ cookiecutter.participant_name_slug }}"]

{% endif -%}
