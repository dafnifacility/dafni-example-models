# Service model example

A service model runs beside other models. 
Typically this can be a database which stores information as a workflow progresses. This example contains two models the service and a model which communicates with it, which we have called the client.

Each model contains:
- _[Dockerfile](./Dockerfile)_ - Builds the service container that will be run by DAFNI
- _[model_definition.yaml](./model_definition.yaml)_ - A machine-readable file used to define the model.

The service model simply starts and runs with an infinite loop, but also outputs the current second. The client model runs a ping command to show it is connecting to the service mode.

The client model expects the service IP to be passed in to the parameter called MY_SERVICE_IP. When both of these models are added to a Workflow, the step name of the service can be added to the client parameter. 

You can build the service model and test is with:
```bash
docker build -t service-example .
docker run servie-example
```

You can build the client model and test it by also passing in an example IP:

```bash
docker build -t client-example .
docker run -e MY_SERVICE_IP=127.0.0.1 client-example
```

## Uploading to DAFNI

You will need to create a file from your docker image to upload it into DAFNI. Check out the detailed instructions online at [Docs](https://docs.secure.dafni.rl.ac.uk/docs/how-to/models/how-to-upload-a-model/) but the basic instructions are as follows:

```bash
docker save -o client-example.tar client-example
docker save -o service-example.tar service-example
```

If you wish you can also compress these file before uploading. This is not essential but for large images it will save you some time when uploading.

```bash
gzip client-example.tar
gzip service-example.tar
```
This will produce files called client-example.tar.gz and service-example.tar.gz

Once in DAFNI you can then upload each of these models by selecting the tar or tar.gz file and their associated mode_definition.yaml files on the "Add Model" page.