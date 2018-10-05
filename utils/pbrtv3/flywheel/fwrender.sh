#!/bin/bash

############
# INPUTS
# 1 - API_KEY
# 2 - Input acquisition ID (download all files in that acquisition) (TODO: ADD TO MATLAB CODE)
# 3 - String containing the acquisition IDs and filenames
# 4 - Output session/acquisition container ID in Flywheel in which to place the outputs.
#     This may be a new session????
############


INPUT_DIRECTORY=$(pwd)/FW_PBRT

if [[ ! -d $INPUT_DIRECTORY ]]; then
  mkdir $INPUT_DIRECTORY
fi

# Download the input data.
python fw_download_input_data "$1" "$2" "$3" "$INPUT_DIRECTORY"

# Render
# 1. If there is a *_depth.pbrt and/or *_mesh.pbrt, then we need to run subsequent runs of pbrt
#    with that reflected in the prbt command, such as "pbrt --outfile $OUTPUT_FILE_depth.dat $INPUT_FILE_depth.pbrt
PBRT_FILES=$(find ${INPUT_DIRECTORY}/* -type f -name "*.pbrt" ! -name "*geometry*" ! -name "*materials*")

cd $INPUT_DIRECTORY
for PBRT_FILE in ${PBRT_FILES}; do

  INPUT_FILE=$(basename ${PBRT_FILE})
  INPUT_FILE_NAME="${INPUT_FILE%.*}"
  OUTPUT_FILE=${INPUT_FILE_NAME}".dat"

  pbrt --outfile ${OUTPUT_FILE} ${INPUT_FILE}

done

# UPLOAD BACK TO FLYWHEEL
# 1 - Find the output_file and label_file (if it exists) and upload to the container in $4
python fw_upload_renderings $1 ${INPUT_DIR} $4
