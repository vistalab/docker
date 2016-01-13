# Create a base docker container that can execute dcm2nii
#
# Example usage:
#   docker run --rm -ti \
#       -v <someDirWithDicoms>:/input \
#       -v <emptyOutputFolder>:/output \
#       vistalab/dcm2nii <optional_flags>
#
# TODO: Configure an opts file
#

# Start with neurodebian image
FROM neurodebian:trusty
MAINTAINER Michael Perry <lmperry@stanford.edu>

# Run apt-get calls
RUN apt-get update \
    && apt-get install -y mricron 

# Configure entrypoint
COPY run /opt/run
ENTRYPOINT ["/opt/run"]

