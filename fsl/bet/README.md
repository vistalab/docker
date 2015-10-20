## vistalab/bet

This dockerfile will create a FSL (v5.0) docker image that executes bet2  


### Build the Image
To build the image, either download the files from this repo or clone the repo:
```
git clone https://github.com/vistalab/docker
cd docker/fsl/bet
./build.sh
```

### Example Usage ###
To run ```bet2``` from this image you can do the following:
```
docker run --rm -ti \
    -v </path/to/input/data>:/input \
    -v </path/to/output>:/output \
    vistalab/bet /input/<t1_file.nii.gz> /output/bet2_
```
* Note that the directory mounted at "/output" must be EMPTY for the algorithm to run. 
* Note that you are mounting the directory (```-v``` flag) which contains your data in the container at ```/input``` and mounting the directory where you want your output data within the container at ```/output```. You may wish to mount a single diretory and use it for both input and output. 
* Note that the `ENTRYPOINT` is configured to be `bet2`, thus only the input arguments need be specified. 



