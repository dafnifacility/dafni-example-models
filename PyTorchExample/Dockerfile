FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

# Use the default Python version in the image (likely 3.6 or 3.7)
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip python3-distutils && \
    python3 -m pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir -p /data/inputs/ /data/outputs/ && chmod -R 777 /data/outputs/

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

COPY test_mnist.py .
COPY test_gpu_torch.py .

ENTRYPOINT ["python3", "-c", "import os; os.system('python3 test_mnist.py && python3 test_gpu_torch.py')"]
