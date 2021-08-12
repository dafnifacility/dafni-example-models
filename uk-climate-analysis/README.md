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
