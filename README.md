# DAFNI Model Examples

This repo contains several simple examples of DAFNI ready models, useful for training or self-paced learning.

 - _[tiny-example--hello-world-model](./tiny-example--hello-world-model)_ 
   - Simplistic linux based model designed to be small in size, it reads one environment variable and outputs a hello message in a text file.
 - _[simple-example--fibonacci-model](./simple-example--fibonacci-model)_ 
   -  Simple Python based model, reading in three environment variables and producing a JSON output file.
 - _[matlab-hello-world-model](./matlab-hello-world-model)_ 
   - Simple hello world example with MATLAB.
 - _[uk-climate-analysis](./uk-climate-analysis)_ 
   - A more complex example model predicting weather from UKCP09 climate projection data. Uses various visualisations to show the results.
 - _[service-example](./service-example)_ 
   - A simple example of both a service model and a normal model communicating.

Instructions are given in each model section, but each follows the same principal steps: you first make edits to the Python source code as required, check the docker and requirements files, create a docker container image and zip it up, then upload this to DAFNI along with the yaml file. This is explained further in the DAFNI [help pages](https://docs.secure.dafni.rl.ac.uk/docs/how-to/models/how-to-create-a-dafni-ready-model/). Note you must also first install Docker on your computer. The open source Docker tools allow you to 'containerise' a model ready to be run on a different computer - thus you prepare the model on your computer, then run it on DAFNI. Docker has an excellent quick start [online guide](https://docs.docker.com/get-started/overview/) which you should read too.
