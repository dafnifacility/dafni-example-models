#!/bin/bash

echo "Copying datasets to working directory"
cp /data/dataslot-name/dataset.csv /code/dataset.csv

echo "Running Hello World Model"
/usr/bin/mlrtapp/helloWorld

echo "Copying outputs to DAFNI outputs directory"
cp /code/output.txt /data/outputs/output.txt

echo "Printing contents of DAFNI outputs directory"
ls -la /data/outputs
