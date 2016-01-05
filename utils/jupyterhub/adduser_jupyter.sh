#!/bin/bash
#
# Add users to a RUNNING Jupyterhub docker container.
# 
# $1 - first arg = container ID or name
# $2 - second arg = username for the user to be added (must be a SUNetID)
#
# EXAMPLE:
#   ./adduser_jupyter.sh jupyter lmperry
#

docker exec $1 adduser --disabled-password --gecos "$2" $2
