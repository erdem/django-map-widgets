FROM ubuntu:14.04

RUN apt-get update && apt-get dist-upgrade -y
RUN apt-get -y install \
    python-pip \
    git \
    python-dev \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    tmux \
    postgresql \
    binutils \
    libproj-dev \
    gdal-bin \
    vim \
    netcat\
    python-virtualenv


WORKDIR /django-map-widgets
ADD conf/requirments-dev.txt /django-map-widgets/requirments-dev.txt
RUN pip install -r requirments-dev.txt
