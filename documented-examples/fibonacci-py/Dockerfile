# base image with Python installed
FROM python:3.9-slim

# set the working directory in the container
WORKDIR /src

# copy the current directory contents into the container
COPY . .

# create the outputs directory
RUN mkdir -p /data/outputs

# define the command to run the script
CMD ["python", "fibonacci.py"]