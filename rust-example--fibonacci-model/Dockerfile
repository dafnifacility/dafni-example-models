# Use the official slim rust docker from docker hub.
FROM rust:slim

COPY fibonacci-model /opt
WORKDIR /opt

RUN cargo build --release

# Tell DAFNI how to run the Model when it starts the container. 
CMD ["target/release/fibonacci-model"]
