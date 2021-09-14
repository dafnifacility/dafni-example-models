# UK Climate Analysis

The code has been adapted from this repo:
https://github.com/aamirpatel23/UK-Climate-Analysis

All of the work on the model is the work of Aamir Patel:
https://github.com/aamirpatel23

The model uses historical data about temperature, rainfall, sunshine and
snowfall to predict the future of the climate in the UK over the next 40 years.

There have been various changes made to the code to make it more usable and
readable in DAFNI.

A Dockerfile has also been added so that the model can run in a container.

The model is based on data from UKCP09 which is downloadable from CEDA (you will need a free account to access and download the data from CEDA). The
datasets needed to run the model for all feature types are listed below:

• https://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-daily/grid/ascii/maximum-temperature

• https://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-daily/grid/ascii/rainfall

• https://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-monthly/grid/ascii/snow-lying

• https://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-monthly/grid/ascii/sunshine

Note, these data have already been loaded into DAFNI, so with the appropriate permissions (just ask us) you can access them directly there to save space. Alternatively download the files from CEDA and file them in your folder structure (noting each of these is a zip file, thus in /data/inputs/rainfall you have 'rainfall.zip' etc.) The data will then be incorporate into the docker image that you upload.

## Creating DOCKER container
After installing Docker on your computer, below are the commands you will need to run to create your docker image of the model ready to upload to DAFNI.
See https://docs.secure.dafni.rl.ac.uk/docs/how-to/models/how-to-create-a-dafni-ready-model/

### Build container
`docker build -t uk-climate-analysis .`

### Run container
`docker run uk-climate-analysis`

### Build image
`docker save -o uk-climate-analysis.tar uk-climate-analysis`

### Compress resultant tar image
`gzip uk-climate-analysis.tar`

This compressed gz file, and the yaml file can now be uploaded to DAFNI via the DAFNI web interface.

## Running the Model
Running the model in DAFNI follows a different mechanism from the text below - the DAFNI `Dockerfile` contains the following two lines:

```
RUN pip install -r requirements.txt
CMD python climate_analysis.py
```

So in DAFNI the model file (climate_analysis.py) is run automatically by the workflow. However, for reference the text below explains how the model could be run on your computer stand-alone.

To run the model 'stand alone', first install the requirements with `pip install -r requirements.txt`. Then, change the `OUTPUT_FOLDER` and `INPUT_FOLDER` in the `climate_analysis.py` file to match your actual data folders.

Then, use `python climate_analysis.py` to run the model.

## Visualising the Model Output
The `visualisation.py` file assumes you have imported the data into a Jupyter notebook but you don't have to do this. You can adapt the `get_output_folder()` folder to point to your output folder instead.

In DAFNI, you will create a new 'Jupyter notebook' in the visualisation tool and then copy and paste in the code from the `visualisation.py` file. In the DAFNI workflow, configure a visualisation to bring over all the data from the model run from path `/data/outputs/*` (this is added in the workflow visualisation setting right at the end of the configuration, below all the metadata settings).

Note to get the `visualisation.py` script to work, you may first need to make some edits (and comment out some lines), such as:

### Editing the Import section
```
import statsmodels.api as sm
#from statsmodels.tsa.base.tsa_model import ValueWarning
#from statsmodels.tools.sm_exceptions import ConvergenceWarning
```

### Editing the Final section
```
for feature_type in ["rainfall", "maximum-temperature", "snow-falling"]:
    # Comment out call to get_output_folder()
    #output_folder = get_output_folder()
    #base_df = pd.read_csv(f"{output_folder}/{feature_type}-base.csv")
    #prediction_df = pd.read_csv(f"{output_folder}/{feature_type}-prediction.csv")
    base_df = pd.read_csv(f"{feature_type}-base.csv")
    prediction_df = pd.read_csv(f"{feature_type}-prediction.csv")
    plot_trend(base_df, feature_type)
    plot_best_fit_line(base_df, feature_type)
    prediction(prediction_df, feature_type, "summer")
```
