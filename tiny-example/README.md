Tiny Model Example
==================

This is a very simplistic model showing the absolute minimum needed to run on DAFNI.
It creates a very small sized model and prints "Hello $NAME".

There are three files here:

 - _[Dockerfile](./Dockerfile)_ - Builds the container that will be run by DAFNI
 - _[model_description.yaml](./model_description.yaml)_ - A machine readable file with defining the model.
   This information will be shown to other users who may wish to use your model.
 - _README.md_ - This helpful file. It should contain detailed information about the model 
   including what it is for, and how to use it.

You can run this example from within the "tiny-example" folder:

```bash
docker build -t tiny-example .
docker run tiny-example
```

You can change the output with the environment variable:

```bash
docker run -e NAME=Matthew tiny-example
```