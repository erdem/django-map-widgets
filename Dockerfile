FROM ubuntu:bionic

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8


RUN apt-get update -qq && apt-get install -y -qq \
    # std libs
    unzip wget sudo less nano curl git gosu build-essential software-properties-common \
    # python basic libs
    python3.8 python3.8-dev python3.8-venv gettext \
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev libgdal-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.8 get-pip.py && rm get-pip.py

RUN ln -s /usr/bin/python3.8 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

COPY conf/requirements-dev.txt /tmp/
RUN pip install -r /tmp/requirements-dev.txt

WORKDIR /data/
WORKDIR /django-map-widgets

COPY conf/web_entrypoint.sh /docker-entrypoint.sh
RUN ["chmod", "+x", "/docker-entrypoint.sh"]
ENTRYPOINT ["/docker-entrypoint.sh"]
