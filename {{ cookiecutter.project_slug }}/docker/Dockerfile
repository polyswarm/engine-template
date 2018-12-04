FROM polyswarm/polyswarm-client

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y unzip

COPY . .

# CUSTOMIZE_HERE
# This is where you would copy you scanner backend binary into the Docker image, e.g.:
# COPY myscanner.bin .

RUN set -x && pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .
CMD ["microengine", "--backend", "{{ cookiecutter.author_org_slug }}_{{ cookiecutter.engine_name_slug }}"]
