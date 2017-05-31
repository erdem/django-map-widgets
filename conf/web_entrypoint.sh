#!/bin/bash
set -e

# Now we need to get the ip address of this container so we can supply it as an environmental
# variable for django so that selenium knows what url the test server is on
# Use below or alternatively you could have used
# something like "$@ --liveserver=$THIS_DOCKER_CONTAINER_TEST_SERVER"

if [[ "'$*'" == *"manage.py test"* ]]  # only add if 'manage.py test' in the args
then
  # get the container id
  THIS_CONTAINER_ID_LONG=`cat /proc/self/cgroup | grep 'docker' | sed 's/^.*\///' | grep -v "docker" | tail -n1`
  # take the first 12 characters - that is the format used in /etc/hosts
  THIS_CONTAINER_ID_SHORT=${THIS_CONTAINER_ID_LONG:0:12}
  # search /etc/hosts for the line with the ip address which will look like this:
  #     172.18.0.4    8886629d38e6
  THIS_DOCKER_CONTAINER_IP_LINE=`cat /etc/hosts | grep $THIS_CONTAINER_ID_SHORT`
  # take the ip address from this
  THIS_DOCKER_CONTAINER_IP=`(echo $THIS_DOCKER_CONTAINER_IP_LINE | grep -o '[0-9]\+[.][0-9]\+[.][0-9]\+[.][0-9]\+')`
  # add the port you want on the end
  # Issues here include: django changing port if in use (I think)
  # and parallel tests needing multiple ports etc.
  THIS_DOCKER_CONTAINER_TEST_SERVER="$THIS_DOCKER_CONTAINER_IP:8081"
  echo "this docker container test server = $THIS_DOCKER_CONTAINER_TEST_SERVER"
  export DJANGO_LIVE_TEST_SERVER_ADDRESS=$THIS_DOCKER_CONTAINER_TEST_SERVER
fi


eval "$@"