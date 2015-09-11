# Create a base freesurfer docker container 
#
# Note: The resulting container is ~8GB. 
# 

# Start with ubuntu
FROM ubuntu:trusty

# Install dependencies for FS
# Download FS_v5.3.0 from MGH and untar to /opt
RUN apt-get update \
&& apt-get -y install tcsh tar wget libgomp1 perl-modules bc \
&& wget -N ftp://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/5.3.0/freesurfer-Linux-centos4_x86_64-stable-pub-v5.3.0.tar.gz \
&& tar -xzvf freesurfer-Linux-centos4_x86_64-stable-pub-v5.3.0.tar.gz -C /opt \
&& rm -f freesurfer-Linux-centos4_x86_64-stable-pub-v5.3.0.tar.gz

# Configure license 
COPY license /opt/freesurfer/.license

# Configure basic freesurfer ENV
ENV FREESURFER_HOME /opt/freesurfer
ENV FSFAST_HOME /opt/freesurfer/fsfast
ENV MNI_PERL5LIB /opt/freesurfer/mni/lib/perl5/5.8.5
ENV FMRI_ANALYSIS_DIR /opt/freesurfer/fsfast
ENV FSF_OUTPUT_FORMAT nii.gz
ENV MINC_BIN_DIR /opt/freesurfer/mni/bin
ENV SUBJECTS_DIR /opt/freesurfer/subjects
ENV PATH /opt/freesurfer/bin:/opt/freesurfer/fsfast/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV MINC_LIB_DIR /opt/freesurfer/mni/lib
ENV MNI_DIR /opt/freesurfer/mni
ENV FIX_VERTEX_AREA= 
ENV MNI_DATAPATH /opt/freesurfer/mni/data
ENV VERRIDE 0
ENV PERL5LIB /opt/freesurfer/mni/lib/perl5/5.8.5
ENV OS Linux
ENV LOCAL_DIR /opt/freesurfer/local

# Configure bashrc to source FreeSurferEnv.sh
RUN /bin/bash -c ' echo -e "source $FREESURFER_HOME/FreeSurferEnv.sh &>/dev/null" >> /root/.bashrc '

