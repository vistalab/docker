## vistalab/hippovol

Uses Matlab (C) Runtime for MatlabR2013a (v.8.1) to execute GLERMA's hippovol code. This code takes a recon-all zip file as input and outputs a zip file with the hippovol stats in ```/output```. Note that no arguments are required for a default run of the code. See ```Params4DockerHippovol.json``` for defaults.

NOTE: THIS CONTAINER DEPENDS ON VISTALAB/FREESURFER-CORE. YOU MUST FIRST BUILD THAT CONTAINER.

### Build ###
To build you can dowload this repo and run ```build.sh``` or run:
```
    docker build --no_cache -t vistalab/hippovol `pwd`
```

### Example Usage ###
```
    docker run --rm -ti \
        -v <zipped_recon-all_folder>:/input \
        -v <empty_folder>:/output \
        vistalab/hippovol 
```

