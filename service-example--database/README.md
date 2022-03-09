# Service model database example

A service model runs alongside other models. 
Typically this can be database which stores information as a workflow progresses.

This example is a more complex model, for a simpler one see the example at [service-example](./../service-example--simple). This contains two models the service and a model which communicates with it, which we have called the client.

The service model contains two files:
- _[Dockerfile](./service/Dockerfile)_ - Builds the database model that will be run by DAFNI
- _[model_definition.yaml](./service/model_definition.yaml)_ - A machine-readable file used to define the model.

The client contains three
- _[Dockerfile](./client/Dockerfile)_ - Builds the client model that will be run by DAFNI
- _[model_definition.yaml](./client/model_definition.yaml)_ - A machine-readable file used to define the model. 
- _[use_database.sh](./client/use_database.sh)_ - This file connects to the database and adds a record.

## Service model
The service model starts up an empty influxdb server and then waits for instructions to come from somewhere. The model_definition also has a readiness_probe set, which allows our system to check the database is ready to be connected to. This particular database can be tested at the url http://<IP>:8086/ping , as shown here:

    spec:
      resources:
        readiness_probe:
          path: /ping
          port: 8086

## Client Model
The client model runs a list of commands from a shell script _use_database.sh_.  The first creates a database (if it doesn't already exist), then adds a record consisting of a single number (between 1 and 100). Lastly it outputs the entire contents of the database to a file.

> **Note:** The client model has been designed so it can be run many times in the same workflow. Each time one is run a new number is added to the database. The last client model run will output **all** the records added by all the client models. 

The client model expects the IP of the service model to be passed in to the client's parameter called `INFLUX_IP` (that environment variable is then used in the _use_database.sh_ file to access the database).

    spec:
      inputs:
        parameters:
          - name: INFLUX_IP
            title: Influx IP
            description: The variable that will hold the IP of the Influx database.
            type: link
            required: false

Every client model (i.e. any model that needs to communicate with a service) needs a parameter of type `link` so the IP address can be passed in and used to communicate.

## In Workflows

When you create a workflow in DAFNI with any service you will have to manually assign the **step name** you chose for the service to any client that needs to access it. This is how communication between client and service is achieved.

For example, you create a workflow with the two models above, one service model step called `my-service` and two client steps called `my-client-1` and `my-client-2`. When adding parameter values you must assign the _link parameter_ called `INFLUX_IP` in each of `my-client-1` and `my-client-2`  to the service step name `my-service`.

## Building

### Service
You can build the service model and test is with:
```bash
docker build -t service-example .
docker run service-example
```
You should see the database start up

### Client 

You can build the client model and test it by also passing in an example IP:

```bash
docker build -t client-example .
docker run -e INFLUX_IP=127.0.0.1 client-example
```

While this should show you some output, it won't actually be able to connect anything until this is used inside a workflow.

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