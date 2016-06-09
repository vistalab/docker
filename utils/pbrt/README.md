# vistalab/pbrt-v2-spectral
> Container with PBRT compiled from [github.com/ydnality/pbrt-v2-spectral/][1]

## Example container usage
Given an input file [ /path/to/your/data/inputdata.pbrt ] run the command below editing the portions within the brackets to match your needs.

```
docker run -t -i --rm \
    -v [/path/to/your/data]:/data \
    vistalab/pbrt-v2-spectral \
    pbrt /data/[inputdata.pbrt] --outfile /data/[outputdata.dat]

```

**PBRT command usage:**

The pbrt command arguments are shown below.

    pbrt [--ncores n] [--outfile filename] [--quick] [--quiet] [--verbose] [--help]<filename.pbrt> ...


   [1]: https://github.com/ydnality/pbrt-v2-spectral/

