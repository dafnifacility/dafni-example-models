FROM ubuntu:18.04
# Copy over a requirements file if needed & install

# Create the data path. Rem. upload input data via web interface in DAFNI.
RUN mkdir -p /data/inputs/
RUN mkdir -p /data/outputs/

# Environment variables
# ENV DECTYP="QALL"

# Install anything needed to compile code (gfortran in this case)
RUN apt-get update
RUN apt-get upgrade
# -y -qq for auto-yes & supressing output noise 
RUN apt-get -y install gfortran

# Copy over code, then compile & run.
COPY pythia6428.f .
COPY main63.f .
RUN f77 -c -o pythia6428.o pythia6428.f
RUN f77 main63.f pythia6428.o

# Note the log contains ascii graphs (v.old school).
CMD ./a.out > log.txt; cp log.txt /data/outputs/
