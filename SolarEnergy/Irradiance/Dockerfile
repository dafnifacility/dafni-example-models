FROM python:3.9
# ENV ISDOCK="Yes"

RUN apt-get update
# Copy over a requirements file if needed & install
COPY requirements.txt .
RUN pip install --no-cache-dir --compile -r requirements.txt

# Create the data path. Rem. upload input data via web interface in DAFNI.
RUN mkdir -p /data/inputs/
RUN mkdir -p /data/outputs/

# Copy over code & run.
COPY main_solar.py .
COPY waypoints.py .
COPY irradiance.py .

CMD python main_solar.py
