# Dataset Download Tool

This document goes over how to use the [Dataset Download Tool](https://github.com/dafnifacility/dataset-download-tool) on the DAFNI platform. The tool enables users to download datasets directly from CEDA archive or Jasmin GWS, and run further models on the downloaded data.

## Pre-requisites

This README should be used as an extention of the [DAFNI documentation](https://docs.secure.dafni.rl.ac.uk/docs/How%20to/how-to-get-started) and any questions should be answered in the main documentation.

### Config file

We will use a config file in order to input arguments and upload it to the dafni platform as a Dataslot. Each model has an inputs folder which has an example file of what config file should look like.

```JSON
    {
        "no_auth":"",
        "url":"https://dap.ceda.ac.uk/path/to/file.nc",
        "checksum":""
    }
```
This file should be saved as `download_args.json`. The possible auth methods: `token`, `username`+`password` or `no_auth`. **NOTE: Any boolean args such as `no_auth` should be "" as this sets it to `True` otherwise it defaults to `False`**. As we are running on the DAFNI platform you should not use the `--dest` (destination) flag otherwise outputs may not be output correctly. 

`username`+`password` example:
```JSON
    {
        "username":"USERNAME",
        "password": "PASSWORD",
        "url":"https://dap.ceda.ac.uk/path/to/file.nc",
        "checksum":""
    }
```
#### Uploading to DAFNI

Go to the Data section and click `Add Data`:

<img src="example_images/dataset_upload.png" width="50%" />

Fill in all the boxes with `*` and ticking `My data is not spatial` and `My data has no dates`. Other fields can be anything and you can input values as you please. 

This dataset can be updated any time with new versions. So any value can be updated when running the workflow in parameters.

**PRIVACY NOTE: If credentails are uploaded DO NOT GIVE ACCESS TO DATASET TO ANYONE. Only you have access to Datasets that you upload**

### Model Definition

An example file is provided, `model_definition.yaml`. In the inputs dataslot add `Dataset Version ID` in the `default` value with ID generated. This ID only needs to be set initially and when uplaoding your model. If you then have to update the `download_args.json` file you can just update the version of the dataset by uploading a new file, then select it in parameters when running the workflow.

## Single Step Model Flow

In this example we setup a single model, which downloads the dataset as well as running a script on the downloaded data. This model first downloads an `.nc` file then runs a basic script which reads the output files.

<img src="example_images/single_step_workflow.png" width="50%" />

`nc-reader` is the model step and `publish-1` shows the output data.

The `single-dafni-model-workflow/model.py` file first sets up the directories and sets up logging these are optional but useful for debugging potential errors.

Then we first download the dataset using subprocess:
```Python
...
#------------------ Run download command and handle any errors ------------------ #
cmd = [
    "dataset-download-tool",
    "--config",
    config_path,
    "--dest", # DO NOT CHANGE OUTPUT PATH WHEN RUNNING ON DAFNI, HERE OR IN CONFIG FILE
    outputs_path, 
    "--log-file",
    LOG_FILE,
]

logger.info("Starting download — command: %s", " ".join(cmd))
try:
    result = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
    )
    logger.info("Download completed successfully.")
    if result.std...
```

Then we execute the nc_reader_example.py

```Python
...nc_cmd = [sys.executable, nc_reader, nc_file]
logger.info("Running nc_reader — command: %s", " ".join(nc_cmd))

# ------------------ Run script and handle any errors ------------------ #
try:
    nc_result = subprocess.run(
        nc_cmd,
        check=True,
        capture_output=True,
        text=True,
    )
    if nc_result.stdout:
        ...
```
These are two steps which we do in a single model and might be appropriate for your use case, if you want to setup complex flows. The `Dockerfile` downloads the `dataset-download-tool` and copies all the required files to run the model.
