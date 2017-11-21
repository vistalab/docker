# Builds //github.com/ydnality/pbrt-v2-spectral/archive/master.zip
#

FROM ubuntu:14.04

MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install pre-requisites
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    openexr \
    openexr-viewers \
    libopenexr-dev \
    libilmbase-dev \
    libfl-dev \
    bison \
    flex \
    git \
    gsl-bin \
    libgsl0-dev \
    wget \
    unzip

# Download and make PBRT
RUN mkdir /pbrt

WORKDIR /pbrt/
RUN wget https://github.com/scienstanford/pbrt-v2-spectral/archive/master.zip
RUN unzip master.zip && rm master.zip

WORKDIR /pbrt/pbrt-v2-spectral-master/src/
RUN make

ENV PATH $PATH:/pbrt/pbrt-v2-spectral-master/src/bin
