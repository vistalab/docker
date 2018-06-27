#!/bin/bash

# 1 - Data directory in google cloud
# 2 - PBRT file to r


# 1 - PBRT file in google cloud

INPUT_FILE=$(basename $1)
INPUT_FILE_NAME="${INPUT_FILE%.*}"
INPUT_DIRECTORY=$(dirname $1)

OUTPUT_FILE=$INPUT_FILE_NAME".dat"

gsutil cp $INPUT_DIRECTORY/*.zip ./
gsutil cp $INPUT_DIRECTORY/*_materials.pbrt ./
gsutil cp $INPUT_DIRECTORY/*_geometry.pbrt ./
gsutil cp $1 ./
unzip *.zip

# Render
pbrt --outfile $OUTPUT_FILE $INPUT_FILE

# Copy the results back to cloud
gsutil cp $OUTPUT_FILE $INPUT_DIRECTORY/renderings/$OUTPUT_FILE
