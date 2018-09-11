FROM python:3.6.4

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y libgeos-dev libgdal-dev
RUN apt-get install -y git-core gcc g++ make libffi-dev libssl-dev python3-dev build-essential libpq-dev libmemcached-dev curl libcairo2-dev
RUN apt-get install -y libtiff5-dev libjpeg-dev libfreetype6-dev webp zlib1g-dev pcre++-dev libpango1.0-dev

RUN apt-get install -y libev-dev
RUN apt-get install -y wget
RUN curl -sL https://deb.nodesource.com/setup_5.x | bashq
:/
RUN apt-get install -y nodejs
RUN pip install --upgrade pip
RUN pip install virtualenv

COPY conf/requirements-dev.txt /tmp/
RUN pip install -r /tmp/requirements-dev.txt

COPY package.json /data/
WORKDIR /data/
RUN npm install
ENV PATH /data/node_modules/.bin:$PATH
WORKDIR /django-map-widgets

COPY conf/web_entrypoint.sh /docker-entrypoint.sh
RUN ["chmod", "+x", "/docker-entrypoint.sh"]
ENTRYPOINT ["/docker-entrypoint.sh"]
