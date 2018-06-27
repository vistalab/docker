# Dockerize Vistalab’s pbrt-v3-spectral. 

FROM ubuntu:14.04

MAINTAINER Trisha Lian <tlian@stanford.edu>
# Adapted from Dockerfile in PBRTv3 repo. 

ENV DEBIAN_FRONTEND=noninteractive

# Install a higher version of cmake
RUN apt-get update -yq
RUN apt-get install -yq software-properties-common
RUN add-apt-repository -y ppa:george-edison55/cmake-3.x
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt-get update
RUN apt-get install cmake -yq

RUN apt-get update -yq
RUN apt-get install -yq build-essential gcc-4.8 g++-4.8 make bison flex libpthread-stubs0-dev zlib1g-dev libgsl0-dev

# Do we need these?
#RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.6
#RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 40 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
#RUN echo 2 | update-alternatives --config gcc

# Setup folder structure
RUN mkdir /pbrt
WORKDIR /pbrt/

# Pull the git directory
RUN apt-get install -y git
RUN git clone --recursive https://github.com/scienstanford/pbrt-v3-spectral.git

WORKDIR /pbrt/pbrt-v3-spectral/build
#RUN cmake -G 'Unix Makefiles' ..
RUN cmake -DCMAKE_BUILD_TYPE=Release ..
RUN make

ENV PATH $PATH:/pbrt/pbrt-v3-spectral/build
