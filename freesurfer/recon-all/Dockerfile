# Create a base docker container that will execute recon-all and zip the output
#
# Example usage:
#   docker run --rm -ti \
#       -v </input/directory>:/input \
#       -v </output/directory>:/output \
#       vistalab/recon-all -i /input/<input_file_name> -subjid <subject_id> -all 
#

# Start with base freesurfer container
FROM vistalab/freesurfer

# Copy the run script
COPY run /opt/run

# Make sure we can execute the script and install zip
RUN chmod +x /opt/run \
    && apt-get update && apt-get -y install zip

# Set entrypoint to run the script
ENTRYPOINT ["/opt/run"]
