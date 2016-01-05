# vistalab/jupyterhub
# 
# Create a Stanford kerberized jupyterhub container with matplotlib (and deps) installed.
#
# Example usage:
#   docker run --rm -p 80:8000 vistalab/jupyterhub 
#
# USER ACCOUNTS:
#   User accounts can be added by running the adduser_jupyter.sh script in this directory.
#   
#   Example: 
#       ./adduser_jupyter.sh jupyter lmperry
#

# TODO: SSL configuration and update python file
#

FROM jupyter/jupyterhub:latest

MAINTAINER Michael Perry <lmperry@stanford.edu>

# Kerberize and install deps for matplotlib
RUN apt-get update && apt-get install -y \
    wget \
    krb5-user libpam-krb5 \
    libpng12-dev libfreetype6-dev \
    && mv /etc/krb5.conf /etc/krb5.conf.dpkg-dist \
    && wget -O /etc/krb5.conf http://web.stanford.edu/dept/its/support/kerberos/dist/krb5.conf \
    && pip install matplotlib --upgrade

# Make notebook directories and make a soft-link to that directory for new users
RUN mkdir -p /srv/jupyterhub/notebooks/ \
    && ln -s /srv/jupyterhub/notebooks /etc/skel/notebooks 

EXPOSE 8000  

ONBUILD ADD jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]

