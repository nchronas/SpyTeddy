FROM resin/rpi-raspbian:wheezy-2015-01-15

# Install Python, pip and the camera module firmware
RUN apt-get update -y && apt-get install -y python python-dev \
libraspberrypi-bin python-pip \
dropbear \
nano \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Install picamera python module using pip
RUN pip install picamera

# add the root dir to the /app dir in the container env
COPY . /app

CMD ["bash", "/app/start.sh"]
