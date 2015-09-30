## vistalab/fsl-v5.0

This dockerfile will create a FSL (v5.0) docker image that can execute any fsl-core command.  


### Build the Image
To build the image, either download the files from this repo or clone the repo:
```
git clone https://github.com/vistalab/docker
cd docker/fsl/fsl-v5.0/
./build.sh
```

### Example Usage ###
To run a "core" command (e.g., `bet2`) from this image you can do the following:
```
docker run --rm -ti \
    -v </path/to/input/data>:/input \
    -v </path/to/output>:/output \
    vistalab/fsl-v5.0 bet2 /input/<t1_file.nii.gz> /output/bet2_
```
* Note that you are mounting the directory (```-v``` flag) which contains your data in the container at ```/input``` and mounting the directory where you want your output data within the container at ```/output```. You may wish to mount a single diretory and use it for both input and output. 




