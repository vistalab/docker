## vistalab/dcm2nii

This dockerfile will create a MRICRON docker image that can execute ```dcm2nii```.  


### Build the Image
To build the image, either download the files from this repo or clone the repo:
```
git clone https://github.com/vistalab/docker
cd docker/utils/dcm2nii
./build.sh
```

### Example Usage ###
To run dcm2nii from this image you can do the following:
```
docker run --rm -ti \
    -v </path/to/input/data>:/input \
    -v </path/to/output>:/output \
    vistalab/dcm2nii /input/<t1_file.nii.gz> 
```
* Note that you are mounting the directory (```-v``` flag) which contains your data in the container at ```/input``` and mounting the directory where you want your output data within the container at ```/output```. You may wish to mount a single diretory and use it for both input and output. 




