FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-devel

# Install dependencies
RUN pip install --upgrade pip
RUN pip install matplotlib tqdm

# Create the data paths
RUN mkdir -p /data/inputs/
RUN mkdir -p /data/outputs/
RUN chmod -R 777 /data/outputs/

# Set environment variables for GPU support
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Copy Python scripts
COPY test_mnist.py .
COPY test_gpu_torch.py .

# Set the entrypoint to run both scripts
ENTRYPOINT ["python", "-c", "import os; os.system('python test_mnist.py && python test_gpu_torch.py')"]
