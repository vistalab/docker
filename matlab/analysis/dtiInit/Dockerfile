# Create Docker container that can run dtiInit analysis. 
# https://github.com/vistalab/vistasoft/tree/master/mrDiffusion/dtiInit/standalone

# Start with the Matlab r2013b runtime container
FROM vistalab/mcr-v82

# ADD the dtiInit Matlab Stand-Alone (MSA) into the container.
ADD https://github.com/vistalab/vistasoft/raw/97aa8a83ea1e89a900e4c6597a404d84f7390b12/mrDiffusion/dtiInit/standalone/executables/dtiInit_glnxa64_v82 /usr/local/bin/dtiInit

# Add bet2 (FSL) to the container
ADD https://github.com/vistalab/vistasoft/raw/f1e7c57bb01bd281be6a8b93cc162994a1307b86/mrAnatomy/Segment/bet2 /usr/local/bin/

# Add the MNI_EPI template and JSON schema files to the container
ADD https://github.com/vistalab/vistasoft/raw/f1e7c57bb01bd281be6a8b93cc162994a1307b86/mrDiffusion/templates/MNI_EPI.nii.gz /templates/
ADD https://github.com/vistalab/vistasoft/raw/97aa8a83ea1e89a900e4c6597a404d84f7390b12/mrDiffusion/dtiInit/standalone/dtiInitStandAloneJsonSchema.json /templates/

# Add the help text to display when no args are passed in.
COPY help.txt /opt/help.txt

# Ensure that the executable files are executable
RUN chmod +x /usr/local/bin/bet2 && chmod +x /usr/local/bin/dtiInit

# Configure environment variables for bet2
ENV FSLOUTPUTTYPE NIFTI_GZ

# Set the entrypoint to the container
ENTRYPOINT ["/usr/local/bin/dtiInit"] 


