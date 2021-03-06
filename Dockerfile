FROM resin/rpi-raspbian:jessie

ENV INITSYSTEM on

RUN echo "deb http://vontaene.de/raspbian-updates/ . main" >> /etc/apt/sources.list


# Install Python, pip and the camera module firmware
RUN apt-get update && apt-get install -y --force-yes python \
python-dev \
libraspberrypi-bin \
python-pip \
python-dbus \
iptables \
python-gobject \
net-tools \
dropbear \
nano \
git \
wget \
tar \
usbutils \
libjpeg8-dev \
imagemagick \
subversion \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Install picamera python module using pip
RUN pip install picamera pyconnman web.py

# add the root dir to the /app dir in the container env
COPY . /app

RUN mkdir /opt/mjpg-streamer && cd /opt/mjpg-streamer/ && svn co https://svn.code.sf.net/p/mjpg-streamer/code/mjpg-streamer/ . && make

#RUN wget https://www.ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 && \
#tar xvf ffmpeg-snapshot.tar.bz2 && \
#cd ffmpeg && \
#./configure && \
#make && \
#make install

#libgstreamer1.0-0 libgstreamer1.0-0-dbg libgstreamer1.0-dev \
#liborc-0.4-0 liborc-0.4-0-dbg liborc-0.4-dev liborc-0.4-doc \
#gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0 \
#gstreamer1.0-alsa gstreamer1.0-doc gstreamer1.0-omx gstreamer1.0-plugins-bad \
#gstreamer1.0-plugins-bad-dbg gstreamer1.0-plugins-bad-doc \
#gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps \
#gstreamer1.0-plugins-base-dbg gstreamer1.0-plugins-base-doc gstreamer1.0-plugins-good \
#gstreamer1.0-plugins-good-dbg gstreamer1.0-plugins-good-doc gstreamer1.0-plugins-ugly \
#gstreamer1.0-plugins-ugly-dbg gstreamer1.0-plugins-ugly-doc gstreamer1.0-pulseaudio \
#gstreamer1.0-tools gstreamer1.0-x libgstreamer-plugins-bad1.0-0 \
#libgstreamer-plugins-bad1.0-dev libgstreamer-plugins-base1.0-0 \
#libgstreamer-plugins-base1.0-dev \

CMD modprobe bcm2835-v4l2
CMD ["bash", "/app/start.sh"]