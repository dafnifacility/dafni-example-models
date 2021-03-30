FROM hello-world:latest

RUN mkdir -p /code
COPY ./src/run_model.sh /code/run_model.sh
RUN chmod 777 /code/run_model.sh
WORKDIR /code

# This is the command that will run your model
ENTRYPOINT ["/code/run_model.sh"]


