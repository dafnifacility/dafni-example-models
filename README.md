# DAFNI Model Examples

This repo contains several simple examples of DAFNI ready models, useful for
training or self-paced learning.

 - _simple-example--fibonacci-model_ - Simple Python based model, reading in
   three environment variables and producing a JSON output file.
 - _matlab-hello-world-model_ - Simple hello world example with matlab.
 - _tiny-example--hello-world_ - Simplistic linux based model designed to be
   small in size, it reads one environment variable and outputs a hello message
   in a text file.
 - _uk-climate-analysis_ - a more complex example model predicting weather from
   UKCP09 climate projection data. Uses various visualisations to show the
   results.

Instructions are given in each model section, but follow the same principal steps, you first make edits to the Python source code as required, check the docker and requirements files, create a docker image and zip it up, then upload to DAFNI along with the yaml file. Note you need to first install Docker on your computer. Docker allows you to 'containerise' a model ready to be run on  a different computer. Docker has an excellent quick start [online guide](https://docs.docker.com/get-started/overview/) which you should read too.
