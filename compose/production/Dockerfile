FROM python:3.6-stretch as django
LABEL mantainer "hacklab/ <contato@hacklab.com.br>"
ENV PYTHONUNBUFFERED 1

# Ensure that the the internal user and
# group used by django have a known uid and gid
RUN groupadd -r -g 999 django \
    && useradd -r -u 999 -g django django

# Geodjango requirements: https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/geolibs/
RUN apt-get update -y && apt-get install -y \
    binutils libproj-dev gdal-bin \
    libgdal-dev

# Needed to build GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

## Install node ##
WORKDIR /tmp
RUN curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh \
    && bash nodesource_setup.sh
RUN apt-get install -y \
                nodejs \
                build-essential \
                gettext \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*
## Finished installing Node ##

# Install Bower
RUN npm install -g bower

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/gunicorn.sh /gunicorn.sh
RUN sed -i 's/\r//' /gunicorn.sh
RUN chmod +x /gunicorn.sh
RUN chown django /gunicorn.sh

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown django /entrypoint.sh

# Install js dependencies
COPY bower.json .
RUN bower --allow-root install
RUN mkdir /app && mv bower_components /app/

COPY . /app

RUN mkdir /app/staticfiles

# env.example must be used during build to provide a valid environment
RUN export $(cat /app/env.example | grep -v ^# | xargs) && \
    python /app/manage.py collectstatic --noinput && \
    python /app/manage.py compress && \
    python /app/manage.py compilemessages

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/gunicorn.sh"]


FROM nginx:1.13 as nginx

COPY ./compose/production/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=django /app/mapaguarani/static/ /usr/share/nginx/html/static/
