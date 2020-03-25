Tiny Model Example
==================

This is a very simplistic model showing the absolute minimum needed to run on DAFNI.
It creates a very small sized model and prints "Hello $NAME".

There are three files here:

 - _[Dockerfile](./Dockerfile)_ - Builds the container that will be run by DAFNI
 - _[model_description.yaml](./model_description.yaml)_ - Details of the model needed by the DAFNI ingest system.
 - _README.md_ - This helpful file.

You can run this example from within the "tiny-example" folder:

```bash
docker build -t tiny-example .
docker run tiny-example
```

You can change the output with the environment variable:

```bash
docker run -e NAME=Matthew tiny-example
```