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


WORKDIR /django-map-widgets/mapwidgets/tests/testapp
COPY conf/requirments-dev.txt /tmp/requirments-dev.txt
RUN pip install -r /tmp/requirments-dev.txt

#COPY conf/web_entrypoint.sh /docker-entrypoint.sh
#RUN ["chmod", "+x", "/docker-entrypoint.sh"]
#ENTRYPOINT ["/docker-entrypoint.sh"]
