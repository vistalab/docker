FROM vistalab/pbrt-v3-spectral

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get install -y python-pip && \
		pip install --upgrade pip && \
		pip install flywheel-sdk

WORKDIR /FW_PBRT
ENV HOME /

# TODO: Copy python functions as well.
COPY fwrender.sh \
    fw_download_input_data.py \
    fw_upload_renderings.py \
    /FW_PBRT/
RUN chmod +x /FW_PBRT/*
