# DAFNI Fortran Example

This is a straightforward example that demonstrates how to dockerise a model, that has been written in fortran77, which can
then be uploaded and run in DAFNI. In order to run this example you will first need to download a copy of 
the code, along with an example run, from the Pythia [website](https://pythia.org/pythia6/#pythia-64) (for those 
interested, Pythia is a particle physics code that simulates what happens when high energy particles collide with 
each other). You will need a copy of these files:

 - [pythia6428.f](https://pythia.org/download/pythia6/pythia6428.f)
 - [main63.f](https://pythia.org/download/pythia6/main63.f)

After downloading the files and ensuring these are in the same directory as the Dockerfile you can proceed with 
dockerising a compiled version pythia using the following commands (the Dockerfile should be very similar for many 
fortran programs).

```
docker build pythia_f77 .
docker save -o pythia_f77.tar pythia_f77
```

and then g-zip'ing the .tar file in preparation for uploading to DAFNI.

Though the parameters in the model_definitions.yaml file are not actually used in the default case (as they will not
be referenced in main63.f), you can use them in the code. For an example of how to do this, the following adjustment
to main63.f, will allow the user to set the number of collisions that are simulated:

```f77
C...Read-in the evironment variable NEVE (which is set in the yaml file).
      CALL getenv('NEVE',NEVE)
C...Main parameters of run: c.m. energy and number of events.
      ECM=91.2D0
      NEV=NEVE
```
