#!/bin/bash

# 1 - Data directory in google cloud
# 2 - Data directory in the container
# 3 - Input file name
# 4 - Output file name
# 5 - ???


# Copy the data from the cloud to a local folder
mkdir -p $2/renderings/PBRTCloud/
gsutil cp $1/$3 $2/

# Unzip data
cd $2
unzip $2/$3

# Render
pbrt --outfile $5 $4

# Copy the rendered .dat file back to the cloud
gsutil cp $5 $1/renderings/PBRTCloud/

DIRNAME=$(dirname $5)
FILENAME=$(basename $5 .dat)
gsutil cp  $DIRNAME/$FILENAME*  $1/renderings/PBRTCloud/

# Remove the data
cd $2 rm -rf ./*
