# Matlab Hello World Model

This is a very simple Model written in Matlab to demonstrate the
process of Dockerising a Matlab Model for upload onto DAFNI.

The Model itself reads a csv file from a Dataset that has been
uploaded to DAFNI, an example of what the csv file looks like,
`dataset.csv`, is included in this folder. The Model then reads
a parameter from the environment variables, parameter values
are passed to Models via environment variables on DAFNI. The 
parameter should contain an integer which will be added 
to the Matrix that is stored in the CSV file. Finally, the
model will write the updated Matrix to a file as an output.

File Structure:

- _[Dockerfile](./Dockerfile)_ - Builds the image that will be
   run by DAFNI
- _[model_definition.yaml](./model_definition.yaml)_ - A 
   human and machine readable file used to define the Model.
   This information will be shown to other users who may wish to 
   use your Model.
- _[dataset.csv](./dataset.csv)_ - an example csv file to run
   the Model with, on DAFNI this file will be provided by a 
   dataset.
- _[helloWorld.m](./helloWorld.m)_ - the Matlab Model code
- _[run_model.sh](./src/run_model.sh)_ - a script that copies
   the input dataset files from DAFNI's data directory to the 
   folder the Model expects the files to be in. It then runs the 
   Model and then copies the output file to DAFNI's data directory
   so DAFNI can find it.

As this Model uses Matlab, the process required to build a Docker
image that can run the Model is more complicated than for the 
other example Models. In fact, the process we use is to generate
a Docker image from Matlab itself and then use that as a base
for the Dockerfile in this folder.

To start with, you will need to have a Linux machine with both
Matlab and Docker installed. The reason you need a Linux machine
is because the Matlab commands needed to produce the Docker image
only work on Linux, as you can see from their
[documentation](https://uk.mathworks.com/help/compiler/package-matlab-standalone-applications-into-docker-images.html).
While you could use this documentation to work out how to dockerise
this Model for yourself I would recommend continuing on with this
README as we have already tweaked the commands to work for DAFNI's
specific use-case.

- Once you have a Linux machine with Matlab and Docker
  installed, copy across `helloWorld.m` into your Matlab workspace.
- We need to make this Matlab script into a standalone 
  application, in order to do this run the following in your Matlab
  console `res = compiler.build.standaloneApplication('helloWorld.m')`
- Now we need to create a DockerOptions object, to do so we need 
  to pass in the object from the previous step and the name you 
  want to use for this intermediate Docker image using:
  `opts = compiler.package.DockerOptions(res,'ImageName','hello-world')`
- To actually create the Docker image from Matlab we need to pass
  the objects produced from the previous two steps into Matlab's
  Docker compiler using: `compiler.package.docker(res, 'Options', opts)`.
  When this command finishes running you can confirm that
  the Docker image has been created properly by running 
  `docker image ls` in a terminal (not your Matlab console). You 
  should see a `hello-world` image listed as well as another image
  or two that Matlab has downloaded for you, you can ignore these
  extra images we only need the `hello-world` image.
- At this point we no longer need Matlab, and all commands from this
  point should be executed in a terminal. Navigate this terminal to 
  your local copy of this folder.
- Once you have your terminal pointing at this folder then you can
  build the Docker image for this Model using 
  ```bash
  docker build -t hello-world-matlab .
  ```
- Given that this Model requires a Dataset as an input, an extra 
  argument needs to be given to Docker in order to test run this
  image. We need to tell Docker to use `dataset.csv` as a volume and to
  mount it at the path that DAFNI would load the dataset into. 
  We can do that using: 
  ```bash
  docker run -e "PARAMETER=5" -v /full/path/to/folder:/data/dataslot-name hello-world-matlab
  ```
  In this command `-e "PARAMETER=5"` provides an environment 
  variable to the running container which emulates the way DAFNI passes
  parameters to Models. `-v /full/path/to/folder:/data/dataslot-name` mounts 
  a folder on your computer, specified on the lefthand side of the colon, to a 
  path inside the Docker image, specified on the righthand side of the colon, 
  you should make sure the path on the lefthand side is the full path to the 
  folder that contains `dataset.csv`. If the command runs successfully, you 
  should see some logs from the Model code telling you what it is doing, 
  there will likely be a couple of errors at the end saying that the 
  `/data/outputs` directory doesn't exist. This is fine, DAFNI creates this 
  directory for you when it runs the Model. You could add another directory 
  mount using a second `-v` argument to your run command, mounting another 
  local folder to `/data/outputs` if you want to test that the copying does 
  work correctly but this isn't necessary.

## Uploading to DAFNI

Now that you have created the docker image for this model you can upload it to
DAFNI. First, you'll need to export the docker image and compress it for 
uploading. The full documentation for this is on our 
[Docs website](https://docs.secure.dafni.rl.ac.uk/docs/how-to/models/how-to-upload-a-model/),
but it can be done using:

```bash
docker save hello-world-matlab | gzip > hello-world-matlab.tar.gz
```
