## vistalab/dtiinit

This dockerfile will create a Docker image that can preprocess diffusion data using the Vistasoft [dtiInit](https://github.com/vistalab/vistasoft/tree/master/mrDiffusion/dtiInit) pipeline. 

### Build the Image
To build the image, either download the files from this repo or clone the repo and run ```build.sh``` or run:
```
docker build --no-cache --tag vistalab/dtiinit `pwd`
```

### Using the image ###
To process a diffusion dataset using this image you should have a raw diffusion data set (nifti, bvecs, and bvals) in a directory (Optionally you can provide an anatomical image to which the diffusion data will be aligned.). You must specify the relative locaitons of these files within either a JSON file, a JSON text string, or a path to a directory containing a JSON file (see ```example.json``` and the [dtiInit standalone wrapper doc string](https://github.com/vistalab/vistasoft/blob/master/mrDiffusion/dtiInit/standalone/dtiInitStandAloneWrapper.m) for more info.) You then pass this file to the Docker container to initiate a dtiInit processing run. 

Note that the minimum required inputs are ```"input_dir"``` and ```"output_dir"```, provided your data can be found within the ```"input_dir"``` and both are mounted as volumes in the container. In this case default values are used. If you want to override one of the defaults, you must specify it in the JSON structure and pass it to the container. 

### Examples
##### Using a JSON file
In this example the required inputs are specified in the JSON file (see the ```example.json``` file in this repo for format and options).
```
docker run --rm -ti \
    -v </input/directory/on/disk>:/input \
    -v </output/directory/on/disk>:/output \
        vistalab/dtiinit \
        /input/<JSON_filename>.json
```
##### Using a JSON string
In this example the required inputs (```"input_dir"``` and ```"output_dir"```) are specified in a JSON string on the command line - note the ```' '``` surrounding the command. 
```
docker run --rm -ti \
    -v </input/directory/on/disk>:/input \
    -v </output/directory/on/disk>:/output \
    vistalab/dtiinit \
    '{"input_dir":"/input", "output_dir": "/output"}'
```
##### Using a directory (in the container) containing a JSON file
In this example a JSON file exists in the '/input/' directory mounted as a volume within the container. 
```
docker run --rm -ti '
    -v </input/directory/on/disk>:/input \
    -v </output/directory/on/disk>:/output \
    vistalab/dtiinit \
    /input/
```

##### Overriding a default parameter
In this example we override one of dtiInit's default values for fitMethod. Note that all other param values not specified are preserved at their default value.
```
docker run --rm -ti \
    -v </input/directory/on/disk>:/input \
    -v </output/directory/on/disk>:/output \
    vistalab/dtiinit \
    '{"input_dir":"/input", "output_dir": "/output", "params": {"fitMethod": "ls"}}'
```

### Building the executable:
To build the dtiInit Executable clone the vistalab/vistasoft repo and download SPM8. Then to build the compiled version of the code: 

`mcc -m <code_path>/vistasoft/mrDiffusion/dtiInit/standalone/dtiInitStandAloneWrapper.m -I <code_path>/vistasoft -I <code_path>/spm8 `

* Note the version downloaded to this container was built on MatlabR2013b


