FROM python:3.8-slim

RUN apt-get update
RUN apt-get install default-jdk -y

RUN mkdir -p /data/outputs/
COPY requirements.txt ./
COPY *.py ./

RUN pip install --no-cache-dir --compile -r requirements.txt
CMD python climate_analysis.py