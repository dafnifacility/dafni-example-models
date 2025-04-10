# About

This is a simple example of a PyTorch model that can be run in DAFNI.

## Build

To build the Docker image, run the following commands:

```bash
docker build -t mnist_pytorch:to-upload .
docker save -o mnist_pytorch.tar mnist_pytorch:to-upload
gzip mnist_pytorch.tar
```

The code can be tested locally by running the docker image:

```bash 
docker run -v $(pwd)/outputs:/data/outputs mnist_pytorch:to-upload
```