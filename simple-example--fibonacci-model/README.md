# Fibonacci Model

This is an example model. Here you should describe what the model does.

This particular model generates a Fibonacci sequence. e.g.:

```
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...]
```

You can set three inputs:

- SEQUENCE_LENGTH - Dictates the count of numbers in the generated sequence
- SEQUENCE_F0 - The first number to start the Fibonacci sequence with.
- SEQUENCE_F1 - The second number to start the Fibonacci sequence with.

The model generates a JSON file containing the sequence:

```json
{
  "sequence": [0, 1, 1, 2, 3, 5]
}
```

## Technical Info

This model pulls in several environment variables and passes them into a piece of Python
code. The Python code is built into a Docker image using the
[provided Dockerfile](./Dockerfile).

There are five files here:

- _[main.py](./src/main.py)_ - This is the file initially called by DAFNI. It is referenced in the
  Dockerfile.
- _[work.py](./src/work.py)_ - This contains the main code for the model. Here, as an example, it is a
  simple Fibonacci generator
- _[Dockerfile](./Dockerfile)_ - Builds the container that will be run by DAFNI
- _[model_definition.yaml](./model_definition.yaml)_ - A machine-readable file used to define the model.
  This information will be shown to other users who may wish to use your model. 
- _README.md_ - This helpful file. It should contain detailed information about the model.

## Dependencies

This model requires [Python](https://www.python.org/) and
[Docker](https://www.docker.com/) to be installed in order to build and run locally.

## Running the Model

You can run this example model from within the "simple-example" folder by doing the
following:

```bash
python ./src/main.py
```

You can also run this model using Docker from within the same folder by doing:

```bash
docker build -t fibonacci-model .
docker run fibonacci-model
```

You don't need to run the build step every time you want to run the model, you only need
to re-run it if changes are made to the Dockerfile or any of the files that go into the
Docker image.

You can adjust the way it runs with the environment variables:

```bash
docker run -e SEQUENCE_LENGTH=50 fibonacci-model
```

or

```bash
docker run -e SEQUENCE_LENGTH=50 -e SEQUENCE_F0=1 -e SEQUENCE_F1=3 fibonacci-model
```

## Uploading to DAFNI

You will need to create a file from your docker image to upload it. Check out the detailed instructions online at [Docs](https://docs.secure.dafni.rl.ac.uk/docs/how-to/models/how-to-upload-a-model/) but you can create it with:

```bash
docker save -o fibonacci-model.tar fibonacci-model
```

You can then also compress it before uploading:

```bash
gzip example-model.tar
```
