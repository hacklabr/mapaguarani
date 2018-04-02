FROM python:3.6-stretch
LABEL mantainer "hacklab/ <contato@hacklab.com.br>"
ENV PYTHONUNBUFFERED 1

# Geodjango requirements: https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/geolibs/
RUN apt-get update -y && apt-get install -y \
    binutils libproj-dev gdal-bin \
    libgdal-dev

## Install node and gettext ##
WORKDIR /tmp
RUN curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh \
    && bash nodesource_setup.sh
RUN apt-get install -y \
                nodejs \
                build-essential \
                gettext \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*
## Finished installing ##

# Install Bower
RUN npm install -g bower

# Needed to build GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /app

# Requirements have to be pulled and installed here, otherwise caching won't work
# ext-apps need to be pulled here too, or live-reloading won't work
COPY ./requirements /app/requirements
COPY ./ext-apps /app/ext-apps
RUN pip install -r /app/requirements/local.txt

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/local/django/runserver.sh /runserver.sh
RUN sed -i 's/\r//' /runserver.sh
RUN chmod +x /runserver.sh

ENTRYPOINT ["/entrypoint.sh"]
