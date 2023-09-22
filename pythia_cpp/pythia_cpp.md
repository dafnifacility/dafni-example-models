# DAFNI C++ Example

This is an example of how to dockerise a model, that has been written in C++, which can then be uploaded and run 
in DAFNI. In order to run this example you will first need to download the code from the 
Pythia [website](https://pythia.org) (for those interested, Pythia is a particle physics code that simulates what 
happens when high energy particles collide with each other). You will need a copy of the main zip file from the webpage:

 - [pythia8310.tgz](https://pythia.org/download/pythia83/pythia8310.tgz)
 
After downloading you can unzip it into a folder (where you should also copy the Dockerfile and .yaml file). At this point
you are ready to dockerise the C++ code (the dockerfile is setup to compile the main libraries on dockerisation, and will
then compile and run the first three examples at runtime).
