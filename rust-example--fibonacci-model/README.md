# Rust Fibonacci Model

This is an example model written in the Rust programming langauge.

This particular model generates a Fibonacci sequence. e.g.:

```
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...]
```

You can set three inputs:

- SEQUENCE_LENGTH - Dictates the count of numbers in the generated sequence
- SEQUENCE_F0 - The first number to start the Fibonacci sequence with.
- SEQUENCE_F1 - The second number to start the Fibonacci sequence with.

The model generates a JSON file containing the sequence, the initial settings and some additional information:

```json
{
  "sequence": [0, 1, 1, 2, 3, 5],
  "settings":  {
    "length": 20,
    "f0": 0,
    "f1": 1
  },
  "model" : {
    "name": "fibonacci-rust-model",
    "version": "1.0",
    "created": "2021-01-27 21:14:56.774076600 UTC"
  } 
}
```

The Rust program uses an `i64` integer and so has a fairly low maximum sequence length value of 93

## Technical Info

This model pulls in several environment variables. The Rust code is built into a Docker image using the
[provided Dockerfile](./Dockerfile).

There are five files here:

 - Rust files:
   - _[main.rs](./fibonacci-model/src/main.rs)_ - This is the main file that is built into a binary.
   - _[work.rs](./fibonacci-model/src/work.rs)_ - This is the file that creates the sequence.
   - _[Cargo.toml](./fibonacci-model/Cargo.toml)_ - This is a Rust Cargo module file.
   - _[Cargo.lock](./fibonacci-model/Cargo.lock)_ - This is a Rust Cargo file to lock dependencies.

- _[Dockerfile](./Dockerfile)_ - Builds the container that will be run by DAFNI
- _[model_definition.yaml](./model_definition.yaml)_ - A machine-readable file used to define the model. This information will be shown to other users who may wish to use your model. 
- _README.md_ - This helpful file. It should contain detailed information about the model.


## Dependencies

This model requires [Rust](https://www.rust-lang.org) and
[Docker](https://www.docker.com/) to be installed in order to build and run locally.

## Running the Model

You can run this example model from within the "simple-example" folder by doing the
following:

```bash
Cargo run
```

You can also run this model using Docker from within the same folder by doing:

```bash
docker build -t fibonacci-rust-model:1.0 .
docker run --rm fibonacci-rust-model:1.0
```

You don't need to run the build step every time you want to run the model, you only need to re-run it if changes are made to the Dockerfile or any of the files that go into the Docker image.

You can change the inputs with environment variables like so:

```bash
docker run -e SEQUENCE_LENGTH=50 -e SEQUENCE_F0=1 -e SEQUENCE_F1=3 fibonacci-rust-model
```

## Uploading to DAFNI

You will need to create a file of your docker image to upload. Check out the detailed instructions online at [Docs](https://docs.secure.dafni.rl.ac.uk/docs/how-to/models/how-to-upload-a-model/) but you can create it with:

```bash
docker save -o fibonacci-rust-model.tar finbonacci-rust-model
```

You can also compress it before uploading:

```bash
gzip fibonacci-rust-model.tar
```
