## vistalab/freesurfer

This docker file will create a Freesurfer image containing all the libs and dependencies required for running Freesurfer. 

NOTE: 
* You MUST read the license agreement and [register with MGH before you use the software](https://surfer.nmr.mgh.harvard.edu/registration.html). 
* once you get your license please edit the license file to add your own license. 
* You can also change ```build.sh``` to change the tag for the image (default=vistalab/freesurfer).**

### Build the Image
To build the image, either download the files from this repo or clone the repo:
```
git clone https://github.com/vistalab/docker
cd docker/freesurfer/v5.3.0-base/
./build.sh
```

### Example Usage ###
To run a Freesurfer command from this image you can do the following:
```
docker run --rm -ti -v </path/to/input/data>:/input -v </path/for/output/data>:/opt/freesurfer/subjects vistalab/freesurfer recon-all -i /input/<t1_file.nii.gz> -subjid <subjectID> -all
```
* Note that you are mounting the directory which contains your data in the container at ```/input``` and mounting the directory where you want your output data at ```/opt/freesurfer/subjects``` - which is Freesurfer's default subjects directory in the container. 

* The namd of the freesurfer executable and the args (relative to the contianer) should be provided at the end of the ```docker run``` command. Remember that if those inputs are files or other resources, those resources must also be mounted in the container and the full path to them (in the container) must be provided. 



