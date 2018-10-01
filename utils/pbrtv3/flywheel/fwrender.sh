#!/bin/bash

# 1 - Data directory in google cloud
# 2 - PBRT file to r


# 1 - PBRT file in google cloud

############
# 1 - API_KEY
# 2 - Input acquisition ID (download all files in that acquisition) (TODO: ADD TO MATLAB CODE)
# 3 - String containing the acquisition IDs and filenames
# 4 - Output session/acquisition container ID in Flywheel in which to place the outputs. 
#     This may be a new session?
############

# Download the input data.
# TODO: Write this in python
INPUT_DIRECTORY=/pbrt_input # Create if not already present
INPUT_FILE=$(fw_download_input_data $1 "$2" $3 $INPUT_DIRECTORY)
# 1. Download all INPUT files in the acquisition with ID=$2
# 2. Download all files in $3 (contianing the ids and filenames)
# 3. Unzip all cgresource files to the INPUT_DIRECTORY
# 4. Resulting in $INPUT_DIRECTORY/scene & $INPUT_DIRECTORY/textures AND $INPUT_DIRECTORY/*.pbrt
# 5. Echo the INPUT_FILE - which is the main pbrt file (not geometry or materials)


# INPUT_FILE=$(basename $1)
INPUT_FILE_NAME="${INPUT_FILE%.*}"
# INPUT_DIRECTORY=$(dirname $1)
EXT=mesh
LABEL_FILE=${INPUT_FILE_NAME}_${EXT}

OUTPUT_FILE=$INPUT_FILE_NAME".dat"
LABEL_FILE=$LABEL_FILE".txt"

# Render
pbrt --outfile $OUTPUT_FILE $INPUT_FILE


# UPLOAD BACK TO FLYWHEEL
fw_upload_renderings $1 $4 
# 1 - Find the output_file and label_file (if it exists) and upload to the container in $4
