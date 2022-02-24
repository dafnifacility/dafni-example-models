# Service model database example

A service model runs alongside other models. 
Typically this can be database which stores information as a workflow progresses.

This example is a more complex model, for a simpler one see the example at [service-example](./../service-example). This contains two models the service and a model which communicates with it, which we have called the client.

The service model contains two files:
- _[Dockerfile](./service/Dockerfile)_ - Builds the database model that will be run by DAFNI
- _[model_definition.yaml](./service/model_definition.yaml)_ - A machine-readable file used to define the model.

The client contains three
- _[Dockerfile](./client/Dockerfile)_ - Builds the client model that will be run by DAFNI
- _[model_definition.yaml](./client/model_definition.yaml)_ - A machine-readable file used to define the model. 
- _[use_database.sh](./client/use_database.sh)_ - This file connects to the database and adds a record.

The service model starts up an empty influxdb server and then waits for instructions to come from somewhere. The model_definition also has a readiness_probe set, which allows out system to check the database is ready to be connected to. This particular database can be tested at the url http://<IP>:8086/ping , as shown here:

    spec:
      resources:
        readiness_probe:
          path: /ping
          port: 8086

The client model runs a list of commands that firsts create a database, then adds a record (a number from 1 to 100), and then outputs the entire database to a file. 

> **Note:** The client model has been designed so it can be run many times in the same workflow. Each time one is run a new number is added to the database.  

The client model expects the service IP to be passed in to the parameter called INFLUX_IP. This is then used in the _use_database.sh_ file.

    spec:
      inputs:
        parameters:
          - name: INFLUX_IP
            title: Influx IP
            description: The variable that will hold the IP of the Influx database.
            type: link
            required: false

When a workflow is being created in DAFNI the **step-name** of the database can be added to the client parameter.

## Building

You can build the service model and test is with:
```bash
docker build -t service-example .
docker run service-example
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