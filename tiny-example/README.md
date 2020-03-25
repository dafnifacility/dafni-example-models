Tiny Model Example
==================

This is a very simplistic model showing the absolute minimum needed to run on DAFNI.
It uses a tiny sized container and prints "Hello NAME". It's ideal for quick testing.

There are five files here:

 - _Dockerfile_ - Builds the container that will be run by DAFNI
 - _model_description.yaml_ - Details of the model needed by the DAFNI ingest system.
 - _README.md_ - This file.

You can run this example from within the "tiny-example" folder:

    docker build -t tiny-example .
    docker run tiny-example
    
You can adjust the way it runs with the environmental variables:

    docker run -e NAME=Matthew tiny-example