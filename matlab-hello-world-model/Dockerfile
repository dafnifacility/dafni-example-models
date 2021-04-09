# This is referring to a local image that is built while following the instructions in the 
# README.md and not image at https://hub.docker.com/_/hello-world
FROM hello-world:latest

RUN mkdir -p /code
COPY ./src/run_model.sh /code/run_model.sh
RUN chmod 777 /code/run_model.sh
WORKDIR /code

# This is the command that will run your model
ENTRYPOINT ["/code/run_model.sh"]


