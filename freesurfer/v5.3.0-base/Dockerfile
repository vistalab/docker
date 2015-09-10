# Create a base freesurfer docker container 
#
# 1. Start with centos6
# 2. Install dependencies for FS
# 3. Download FS_v5.3.0 from MGH and untar to /opt
# 4. Configure license 
# 5. Configure ENV
# 6. Configure bashrc to source FreeSurferEnv.sh
#
# Note: The resulting container is ~8GB. The centos6 image is (<200mb)
# 

FROM centos:6

RUN yum -y install tar wget libgomp &>/dev/null \
&& wget -N ftp://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/5.3.0/freesurfer-Linux-centos4_x86_64-stable-pub-v5.3.0.tar.gz \
&& tar -xzvf freesurfer-Linux-centos4_x86_64-stable-pub-v5.3.0.tar.gz -C /opt \
&& rm -f freesurfer-Linux-centos4_x86_64-stable-pub-v5.3.0.tar.gz

# This license should be swapped out for any other user!
COPY license /opt/freesurfer/.license

# Optionally the license file can be written in line.
# RUN /bin/bash -c 'echo -e "lmperry@stanford.edu\n7837\n *CEVUM2TwI7g2" > /opt/freesurfer/.license'

ENV FREESURFER_HOME /opt/freesurfer
RUN /bin/bash -c ' echo -e "source $FREESURFER_HOME/FreeSurferEnv.sh &>/dev/null" >> /root/.bashrc '


