#!/bin/bash

############
# Positional Arguments
# 1 - API_KEY
# 2 - Input acquisition ID (we download all files in that acquisition)
# 3 - String containing the acquisition IDs and filenames
# 4 - Output project ID in Flywheel in which to place the outputs.
# 5 - Session Label - this will be the label used for the Session in FLYWHEEL
# 6 - Acquisition label - this will the label used for the acquisition in FLYWHEEL
# 7 - Subject Label - this will be used to set the subject label/code in FLYWHEEL

# Example usage:
#    fwrender.sh <API_KEY> \
#                5dd319a5fd5f730040fe7f8b \
#                '5dd319a5fd5f730040fe7f8b city4_9:30_v0.0_f40.00front_o270_materials.pbrt' \
#                5c2df7a933cc940062d70d6c \
#                city4_9:30_v0.0_f40.00front_o270 \
#                city4 \
#                renderings
############


INPUT_DIRECTORY=/FW_PBRT

if [[ ! -d $INPUT_DIRECTORY ]]; then
  mkdir $INPUT_DIRECTORY
fi

# Download the input data.
python /code/fw_download_input_data.py "$1" "$2" "$3" "$INPUT_DIRECTORY"

# Render
# 1. If there is a *_depth.pbrt and/or *_mesh.pbrt, then we need to run subsequent runs of pbrt
#    with that reflected in the prbt command, such as "pbrt --outfile $OUTPUT_FILE_depth.dat $INPUT_FILE_depth.pbrt
PBRT_FILES=$(find ${INPUT_DIRECTORY}/* -maxdepth 0 -type f -name "*.pbrt" ! -name "*geometry*" ! -name "*materials*")

cd $INPUT_DIRECTORY
for PBRT_FILE in ${PBRT_FILES}; do

  INPUT_FILE=$(basename ${PBRT_FILE})
  INPUT_FILE_NAME="${INPUT_FILE%.*}"
  OUTPUT_FILE=${INPUT_FILE_NAME}".dat"

  pbrt --outfile ${OUTPUT_FILE} ${INPUT_FILE}

done

# Handle the session label parameter
if [[ -z "$5" ]]; then
  session_label='null'
else
  session_label="$5"
fi

# Handle the acquisition label parameter
if [[ -z "$6" ]]; then
  acquisition_label=${INPUT_FILE_NAME}
  if [[ ${acquisition_label} == *"_mesh"* ]]; then
    acquisition_label=$(basename ${acquisition_label} _mesh)
  elif [[ ${INPUT_FILE_NAME} == *"_depth"* ]]; then
    acquisition_label=$(basename ${acquisition_label} _depth)
  fi
else
  acquisition_label="$6"
fi

# Handle the subject label parameter
if [[ -z "$7" ]]; then
  subject_label='null'
else
  subject_label="$7"
fi


# UPLOAD BACK TO FLYWHEEL
# 1 - Find the output_file and label_file (if it exists) and upload to the container in $4
python /code/fw_upload_renderings.py "$1" "${INPUT_DIRECTORY}" "$4" "${acquisition_label}" "${session_label}" "${subject_label}"
