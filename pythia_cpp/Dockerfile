FROM ubuntu:18.04
# Copy over a requirements file if needed

# Create the data path. Rem. upload input data via web interface in DAFNI.
RUN mkdir -p /data/inputs/
RUN mkdir -p /data/outputs/

# Environment variables

# Install anything needed for build
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install build-essential

# Copy over code.
COPY ./configure /home/pythia8308/
COPY ./Makefile /home/pythia8308/
COPY ./pythia8-config.inc /home/pythia8308/
COPY ./AUTHORS /home/pythia8308/
COPY ./CODINGSTYLE /home/pythia8308/
COPY ./COPYING /home/pythia8308/
COPY ./GUIDELINES /home/pythia8308/
COPY ./README /home/pythia8308/

COPY ./examples/ /home/pythia8308/examples/
COPY ./include/ /home/pythia8308/include/
COPY ./plugins/ /home/pythia8308/plugins/
COPY ./share/ /home/pythia8308/share/
COPY ./src/ /home/pythia8308/src/

RUN ls --recursive /home/pythia8308/

# Compile libs
WORKDIR /home/pythia8308
RUN ./configure
RUN make
# Compile first set of examples and run. Copy output to data folder.
WORKDIR /home/pythia8308/examples
ENTRYPOINT ./runmains --run="01 02 03"; cp main*.log /data/outputs/; cp main03plot.py /data/outputs/; cp out03plot*.dat /data/outputs/; ls /data/outputs/


