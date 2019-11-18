# debug mode, should change back to
FROM vistalab/pbrt-v3-spectral

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y -qq --no-install-recommends wget unzip python php5-mysql php5-cli php5-cgi openjdk-7-jre-headless openssh-client python-openssl && apt-get clean

RUN apt-get install -y python-pip && \
		pip install --upgrade pip && \
		pip install flywheel-sdk && \
		pip install -U crcmod &&\
		pip install pytz &&\
		pip install tzlocal

WORKDIR /FW_PBRT
ENV HOME /
ENV CLOUDSDK_PYTHON_SITEPACKAGES 1
RUN wget --no-check-certificate https://dl.google.com/dl/cloudsdk/channels/rapid/google-cloud-sdk.zip && unzip google-cloud-sdk.zip && rm google-cloud-sdk.zip
RUN google-cloud-sdk/install.sh --usage-reporting=true --path-update=true --bash-completion=true --rc-path=/.bashrc --additional-components app-engine-java app-engine-python app kubectl alpha beta pubsub-emulator cloud-datastore-emulator app-engine-go


# Disable updater check for the whole installation.
# Users won't be bugged with notifications to update to the latest version of gcloud.
RUN google-cloud-sdk/bin/gcloud config set --installation component_manager/disable_update_check true

# TODO: Copy python functions as well.
RUN mkdir /code
COPY fwrender.sh \
    fw_download_input_data.py \
    fw_upload_renderings.py \
    /code/
RUN chmod +x /code/*
