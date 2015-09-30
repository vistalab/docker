## vistalab/dcm-convert
Converts raw MR DICOM data, from Siemens or GE, to NIfTI. 

This container consists of the python package, `scitran.data`. The `run` entrypoint is configured to accept a semi-standard input filetype, a `tgz`, that contains raw data and a `json` file that indicates the raw data filetype, header data, and metadata corrections and an output base directory where results will be saved.

### Usage
`vistalab/dcm-convert` accepts three inputs: `<path_to_dicom_tgz>` `<outfile_name_prefix>` `<log_level[=info]>`

The following will take the raw, tarred and zipped, DICOM input **<input.tgz>** and convert it to nifti, **<outprefix.nii.gz>**.

```
    docker run --rm -ti \
        -v /path/to/dicom/data:/data \
        vistalab/dcm-convert \
        /data/input.tgz \
        /data/outprefix
```

### Resources
Note that the run command in this container is the ~equivelant to installing [Scitran Data](https://github.com/scitran/data) and running the following command in python.

```
    import scitran.data as scidata
    ds = scidata.parse('/path/to/input.gz', filetype='dicom')
    ds.load_data()
    scidata.write(ds, ds.data, 'outprefix', filetype='nifti')
```

For more information on using Scitran Data in bash, see the [CLI tutorial](https://scitran.github.io/cli_tutorial.html).

For more information on using Scitran Data in python see the [Python tutorial](https://scitran.github.io/nimsdata/python_tutorial.html).
