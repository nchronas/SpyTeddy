FROM resin/rpi-raspbian:wheezy-2015-01-15

# Install Python, pip and the camera module firmware
RUN apt-get update && apt-get install -y python \
python-dev \
libraspberrypi-bin \
python-pip \
dropbear \
nano \
git autoconf automake libtool gtk-doc-tools libglib2.0-dev \
libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Install picamera python module using pip
RUN pip install picamera

RUN git clone git://anongit.freedesktop.org/gstreamer/gst-omx && cd gst-omx && ./autogen.sh

# add the root dir to the /app dir in the container env
COPY . /app

CMD ["bash", "/app/start.sh"]
