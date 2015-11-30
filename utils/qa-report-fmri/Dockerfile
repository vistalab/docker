# vistalab/qa_report_fmri
#
# Use NIMS code from Bob Dougherty to create a qa_report for a given fmri NIfTI file.
# See https://github.com/cni/nims/blob/master/nimsproc/qa_report.py for original source code.
#
# Example usage:
#   docker run --rm -ti \
#        -v /path/nifti_file:/input \
#        vistalab/qa_report_fmri /input -i nifti_file.nii.gz
#

FROM ubuntu-debootstrap:trusty

MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install dependencies
RUN apt-get update && apt-get -y install python-dev \
   git \
   libjpeg-dev \
   zlib1g-dev \
   pkg-config \
   libpng12-dev \
   libfreetype6-dev

# Link libs: pillow jpegi and zlib support hack
RUN ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
RUN ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

# Install scitran.data dependencies
RUN apt-get -y install \
    python-numpy \
    python-pip \
    python-scipy \
    python-dipy \
    python-nipy \
    python-nibabel \
    zip \
    unzip

RUN  pip install dipy --upgrade \
    && pip install nipy --upgrade \
    && pip install matplotlib --upgrade

COPY qa_report_sa.py /opt/qa_report.py
COPY run /scripts/run

ENTRYPOINT ["/scripts/run"]
