# Hello World Model

This is a very simplistic model showing the absolute minimum needed to run on DAFNI.
It creates a very small sized model and prints "Hello $NAME".

There are three files here:

 - _[Dockerfile](./Dockerfile)_ - Builds the container that will be run by DAFNI
 - _[model_definition.yaml](./model_definition.yaml)_ - A machine-readable file used to define the model.
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

## Uploading to DAFNI

You will need to create a file from your docker image to upload it. Check out the detailed instructions online at [Docs](https://docs.secure.dafni.rl.ac.uk/docs/how-to/models/how-to-upload-a-model/) but you can create it with:

```bash
docker save -o tiny-example.tar tiny-example
```

You can also compress the `tiny-example.tar` file before uploading. This is not essential but for large images it will save you some time when uploading.

```bash
gzip tiny-example.tar
```