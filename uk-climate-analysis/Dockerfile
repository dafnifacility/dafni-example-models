FROM python:3.8

RUN apt-get update
RUN apt-get install default-jdk -y

RUN mkdir -p /data/outputs/
COPY requirements.txt ./
COPY *.py ./
COPY uk_regions_map.geojson /data/outputs/

RUN pip install -r requirements.txt
CMD python climate_analysis.py