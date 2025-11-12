# use an official GCC image as the base image
FROM gcc:latest


# install required libraries (e.g., jsoncpp for JSON handling)
RUN apt-get update && apt-get install -y \
    libjsoncpp-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libjsoncpp-dev \
    && rm -rf /var/lib/apt/lists/*

# set the working directory in the container
WORKDIR /src

# copy the current directory contents into the container
COPY . .

# compile the C++ code
RUN g++ -std=c++17 -o fibonacci fibonacci.cpp -I/usr/include/jsoncpp -L/usr/lib/x86_64-linux-gnu -ljsoncpp

# create output directory
RUN mkdir -p /data/outputs

# define the command to run the compiled application
CMD ["./fibonacci"]
