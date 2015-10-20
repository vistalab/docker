# Create a base docker container that will run fast.
#
# Example usage:
#    docker run --rm -ti \
#        -v </path/to/input/data>:/input \
#        -v </path/to/output>:/output \
#        vistalab/fast -v --out=/output/<out_base_name> /input/<t1_file.nii.gz>  
#

# Start with FSL image
FROM vistalab/fsl-v5.0
MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install zip
RUN apt-get update && apt-get install -y zip

# Put run script in place
COPY run /opt/run

# Configure entrypoint
ENTRYPOINT ["/opt/run"]

# Configure timezone
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
