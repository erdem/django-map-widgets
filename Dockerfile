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
    python-virtualenv \
    nodejs \
    npm

RUN sudo ln -s "$(which nodejs)" /usr/bin/node

COPY conf/requirements-dev.txt /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements-dev.txt

COPY package.json /data/
WORKDIR /data/
RUN npm install
ENV PATH /data/node_modules/.bin:$PATH


COPY conf/web_entrypoint.sh /docker-entrypoint.sh
RUN ["chmod", "+x", "/docker-entrypoint.sh"]
ENTRYPOINT ["/docker-entrypoint.sh"]
