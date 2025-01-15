# French Traffic Example

Build and run the model

```sh
docker build -t french-traffic-example .
```

Create image for DAFNI

```sh
docker save -o french-traffic-example.tar french-traffic-example
gzip french-traffic-example.tar 
```

Once the dataset `BAAC_2021.xlsx` is uploaded to the DAFNI platform, a data version ID will be generated. 
This ID must be updated in the `model_definition.yaml` file before uploading the model to the DAFNI platform.
For more details, please refer to the DAFNI documentation.
