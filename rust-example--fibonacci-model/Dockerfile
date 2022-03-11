# Use the official slim rust docker from docker hub.
FROM rust:alpine

COPY fibonacci-model /tmp
WORKDIR /tmp

# Build the release
RUN cargo build --release

# Clean up files
RUN mv target/release/fibonacci-model /opt
RUN rm -rf /tmp/*

WORKDIR /opt

# Tell DAFNI how to run the Model when it starts the container. 
CMD ["/opt/fibonacci-model"]
