## vistalab/recon-all

This dockerfile will create a Freesurfer (v5.3.0) docker image that executes ```recon-all``` and compresses the outputs.  

* You MUST read and agree to the license agreement and [register with MGH before you use the software](https://surfer.nmr.mgh.harvard.edu/registration.html). 
* Once you get your license please edit the license file to reflect your license. 
* You can also change ```build.sh``` to edit the tag for the image (default=vistalab/recon-all).
* The resulting image is ~8GB

### Build the Image
To build the image, either download the files from this repo or clone the repo:
```
git clone https://github.com/vistalab/docker
cd docker/freesurfer/recon-all/
./build.sh
```

### Entrypoint ###
An 'Entrypoint' has been configured for this image at ```/opt/run```, which will do the following:
1. Look for inputs and show help as necessary 
2. Run ```recon-all``` using the inputs provided
3. Compress (using ```zip```) all the outputs generated
4. Remove the uncompressed outputs


### Example Usage ###
To run ```recon-all``` from this image you can do the following (note that the ```recon-all``` command is omitted as it is called from the ```Entrypoint```):
```
docker run --rm -ti \
    -v </path/to/input/data>:/input \
    -v </path/for/output/data>:/ouput \
    vistalab/recon-all -i /input/<t1_file.nii.gz> -subjid <subjectID> -all
```
* Note that you are mounting the directory (```-v``` flag) which contains your data in the container at ```/input``` and mounting the directory where you want your output data within the container at ```/output```.

* ```recon-all``` args (relative to the contianer) should be provided at the end of the ```docker run``` command, as shown above. Remember that if those inputs are files or other resources, they must also be mounted in the container and the full path to them (again, relative to the container) must be provided. 



