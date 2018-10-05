FROM vistalab/pbrt-v3-spectral

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install -y python-pip && \
		pip install --upgrade pip && \
		pip install flywheel-sdk

WORKDIR /
ENV HOME /

# TODO: Copy python functions as well.
COPY fwrender.sh /
RUN chmod +x /fwrender.sh
