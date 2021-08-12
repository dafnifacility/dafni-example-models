# UK Climate Analysis

The code has been adapted from this repo:
https://github.com/aamirpatel23/UK-Climate-Analysis

All of the work on the model is the work of Aamir Patel:
https://github.com/aamirpatel23

The model uses historical data about temperature, rainfall, sunshine and
snowfall to predict the future of the climate in the UK over the next 40 years.

There have been various changes made to the code to make it more usable and
readable.

A Dockerfile has also been added so that the model can run in a container.

The model is based on data from UKCP09 which is downloadable from CEDA. The
datasets needed to run the model for all feature types are listed below:

• https://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-daily/grid/ascii/maximum-temperature

• https://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-daily/grid/ascii/rainfall

• https://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-monthly/grid/ascii/snow-lying

• https://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-monthly/grid/ascii/sunshine

## Running the Model
To run the model, first install the requirements with `pip install -r
requirements.txt`. Then, change the `OUTPUT_FOLDER` and `INPUT_FOLDER` in the
`climate_analysis.py` file to match your actual data folders. 

Then, use `python climate_analysis.py` to run the model. 

The `visualisation.py` file assumes you have imported the data into a Jupyter
notebook but you don't have to do this. You can adapt the `get_output_folder()`
folder to point to your output folder instead.