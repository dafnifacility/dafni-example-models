# Use a tiny linux distribution
FROM alpine

RUN mkdir -p /data/outputs/

# Set a default value for the environment variable NAME. This can be overriden at run time.
ENV NAME="World"

# Tell Docker what to run when the Model starts. 
CMD ["/bin/sh", "-c", "echo Hello ${NAME} | tee /data/outputs/hello.txt"]
