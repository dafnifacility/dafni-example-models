FROM python:3.12-slim
WORKDIR /src

ARG GITHUB_TOKEN

RUN apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/* && \
    pip install numpy pandas netCDF4 --no-cache-dir --upgrade pip && \
    pip install "git+https://${GITHUB_TOKEN}@github.com/dafnifacility/dataset-download-tool.git"

COPY model.py model.py
COPY nc_reader_example.py nc_reader_example.py

RUN mkdir -p /data/outputs

CMD ["python", "model.py"]