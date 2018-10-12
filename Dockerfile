FROM raspbian/stretch

RUN apt-get update \
    && apt-get -y install python3 \
    python3-pip \
    python3-dev \
    python3-rpi.gpio \
    python3-pyqt5 build-essential \
    git

RUN apt-get install -y software-properties-common vim


RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /workspace
ADD . .
RUN pip3 install -r requirements.txt
RUN chmod -R a+w /workspace

EXPOSE 8000
EXPOSE 10654
EXPOSE 8888
EXPOSE 5000
EXPOSE 9999