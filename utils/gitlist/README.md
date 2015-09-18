## vistalab/gitlist

Build a docker image that can provide a webUI for a git repo using GitList (http://gitlist.org).

## Build
Clone the repo and:
```
cd docker/utils/gitlist
./build.sh
```

### Usage notes
To use this image you must mount a directory (volume) containing git repositories to ```/repos``` in the container (see example below).

### Example usage:
Start the container
```
  docker run -d \
      -name gitlist
      -p 80:80 \
      -v <repos/on/disk>:/repos \
      vistalab/gitlist
```
Stop the container
```
  docker stop gitlist
```
