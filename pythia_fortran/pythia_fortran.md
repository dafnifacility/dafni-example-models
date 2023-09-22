# DAFNI Fortran Example

This is a straightforward example that will demonstrate how to dockerise a model written in fortran77, which can
then be uploaded and run in DAFNI. First in order to run this example you will first need to download a copy of 
the code from the Pythia [website](https://pythia.org/pythia6/#pythia-64) (for those interested in what this code 
does, Pythia is a particle physics code that simulates what happens when high energy particles collide with each other). 
You will need a copy of :

 - [pythia6428.f](https://pythia.org/download/pythia6/pythia6428.f)
 - [main63.f](https://pythia.org/download/pythia6/main63.f)

After downloading the files and ensuring these are in the same directory as the Dockerfile you can proceed with 
dockerising a compiled version of the code using the following commands.

docker build pythia_f77 .
docker save -o pythia_f77.tar pythia_f77

and then g-zip'ing the .tar file in preparation for uploading to DAFNI.

Though the parameters in the model_definitions.yaml file are not actually used in this particular case (as they will not
be referenced in main63.f. If you wanted to use them in the code then you could access them with the following adjustment
to main63.f (this for instance allows the user to set the number of collisions):

C...Read-in the evironment variable NEVE (which is set in the yaml file.
      CALL getenv('NEVE',NEVE)
C...Main parameters of run: c.m. energy and number of events.
      ECM=91.2D0
      NEV=NEVE
