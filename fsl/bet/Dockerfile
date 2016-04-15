# Create a base docker container that will run bet2
#
# Example usage:
#   docker run --rm -ti \
#       vistalab/bet <input_fileroot> <output_fileroot> [options]
#

# Start with FSL image
FROM vistalab/fsl-v5.0

# Put run in place
COPY run /opt/run

# Configure entrypoint
ENTRYPOINT ["/opt/run"]

# Set a timezone (used in zip file name)
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

