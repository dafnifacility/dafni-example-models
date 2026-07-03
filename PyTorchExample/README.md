# About

This is a simple example of a PyTorch model that can be run in DAFNI.

## Build

To build the Docker image, run the following commands:

```bash
docker build -t pytorch_mnist_model:to-upload .
docker save -o pytorch_mnist_model.tar pytorch_mnist_model:to-upload
gzip pytorch_mnist_model.tar
```

The code can be tested locally by running the docker image:

```bash 
If your local environment has access to a GPU, the code can be tested locally by running the docker image:

```bash
docker run --gpus all -v $(pwd)/outputs:/data/outputs pytorch_mnist_model:to-upload
```