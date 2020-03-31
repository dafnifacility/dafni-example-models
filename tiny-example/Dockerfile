# Use a tiny linux distribution
FROM alpine

RUN mkdir -p /data/outputs/
ENV NAME="DAFNI"

# Tell Docker what to run when the Model starts. 
CMD ["/bin/sh", "-c", "echo Hello ${NAME} | tee /data/outputs/hello.txt"]
