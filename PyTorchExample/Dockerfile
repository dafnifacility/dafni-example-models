FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install Python 3.10 and minimal system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3.10 python3-pip python3-distutils && \
    ln -sf python3.10 /usr/bin/python3 && \
    python3 -m pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install only uv and minimal dependencies
RUN pip install uv

COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml \
    && rm -rf /root/.cache/uv

# Remove docs, tests, examples, __pycache__, etc. (adjust path if needed)
RUN for d in /usr/local/lib/python3.10/dist-packages /usr/lib/python3/dist-packages; do \
    if [ -d "$d" ]; then \
        find "$d" -type d -name 'tests' -exec rm -rf {} +; \
        find "$d" -type d -name '__pycache__' -exec rm -rf {} +; \
        find "$d" -type d -name 'test' -exec rm -rf {} +; \
        find "$d" -type d -name 'docs' -exec rm -rf {} +; \
        find "$d" -type d -name 'examples' -exec rm -rf {} +; \
        find "$d" -type f -name '*.pyc' -delete; \
    fi; \
done

RUN mkdir -p /data/inputs/ /data/outputs/ && chmod -R 777 /data/outputs/

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

COPY test_mnist.py .
COPY test_gpu_torch.py .

ENTRYPOINT ["python3", "-c", "import os; os.system('python3 test_mnist.py && python3 test_gpu_torch.py')"]
