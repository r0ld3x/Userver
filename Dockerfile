# syntax=docker/dockerfile:1

# FROM redis
FROM ubuntu:bionic
FROM python:3.8-slim-buster
FROM theteamultroid/ultroid:main

LABEL Maintainer="r0ld3x"

RUN apt-get --yes --force-yes update && apt-get --yes --force-yes upgrade && apt-get  install --yes --force-yes python3-pip g++  rsync make
# RUN apt-get -y  --force-yes install build-essential git cmake autoconf pkg-config cython python3-dev
# RUN apt-get --yes --force-yes update && apt-get --yes --force-yes upgrade && apt-get autoremove && apt-get autoclean 
# RUN apt-get --yes --force-yes install clang && apt-get --yes --force-yes install build-essential && apt-get --yes --force-yes install manpages-dev && apt-get  --yes --force-yes install python-dev && apt-get --yes --force-yes install python3-dev
RUN apt-get install --yes --force-yes bash build-essential cmake curl debian-archive-keyring debian-keyring ffmpeg gcc git gnupg jq libatlas-base-dev libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libboost-python-dev libcurl4-openssl-dev libffi-dev libgconf-2-4 libgtk-3-dev libjpeg-dev libjpeg62-turbo-dev libopus-dev libopus0 libpq-dev libreadline-dev libswresample-dev libswscale-dev libssl-dev libwebp-dev libx11-dev libxi6 libxml2-dev libxslt1-dev libyaml-dev linux-headers-amd64 make mediainfo megatools meson musl musl-dev neofetch ninja-build openssh-client openssh-server openssl p7zip-full pdftk pkg-config procps python3-dev texinfo unzip util-linux wget wkhtmltopdf xvfb yasm zip zlib1g zlib1g-dev 
RUN apt-get install --yes --force-yes python3-distutils python-distutils python-distutils-extra python3-apt
RUN pip3 install pip --upgrade 
RUN pip3 install --upgrade setuptools wheel

RUN git clone https://github.com/r0ld3x/Userver.git /root/Userver/
# RUN pip install --upgrade pip setuptools wheel
# RUN pip3 install --upgrade setuptools wheel
# RUN python3 -m pip install --upgrade pip
RUN pip uninstall -y numpy
RUN pip install --no-cache-dir -r root/Userver/requirements.txt


WORKDIR /root/Userver/

CMD [ "bash" , "start.sh"]


