FROM polyswarm/polyswarm-client

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y unzip

COPY . .
# todo edit in here if you need a backend

RUN set -x && pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .
CMD ["microengine", "--backend", "{{ cookiecutter.author_org_slug }}_{{ cookiecutter.engine_name_slug }}"]
