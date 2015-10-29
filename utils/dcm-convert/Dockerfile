# vistalab/dcm-convert
# 
# Use Scitran Data to convert raw DICOM data (tgz) from Siemens or GE to NIfTI.
# See http://github.com/scitran/data for source code.
#
# Example usage:
#   docker run --rm -ti \
#        -v /path/to/dicom/data:/data \
#        vistalab/dcm-convert \
#        /data/input.tgz \
#        /data/outprefix
#

FROM ubuntu-debootstrap:trusty

MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install dependencies
RUN apt-get update && apt-get -y install python-dev \
   python-virtualenv \
   git \
   libjpeg-dev \
   zlib1g-dev

# Link libs: pillow jpegi and zlib support hack
RUN ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
RUN ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

# Install scitran.data dependencies
RUN pip install \
    numpy==1.9.0 \
    pytz \
    pillow \
    git+https://github.com/scitran/pydicom.git@0.9.9_value_vr_mismatch \
    git+https://github.com/nipy/nibabel.git@3bc31e9a6191fc54667b3387ed5dfaced46bf755 \
    git+https://github.com/moloney/dcmstack.git@6d49fe01235c08ae63c76fa2f3943b49c9b9832d \
    git+https://github.com/scitran/data.git@2c420ab5d84f311c1480731c67c6a6fb7012c511

# Clone scripts
RUN git clone https://github.com/scitran/scripts.git /root/scripts \
    && cd /root/scripts \
    && git reset --hard fd6afcc90b02eab8372541475d2caa8b40d3bee6

COPY ./run ./scripts/run

ENTRYPOINT ["/scripts/run"]
