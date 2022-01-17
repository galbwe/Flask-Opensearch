FROM ubuntu:18.04

# install python 3.6 and 3.7
# TODO: add more recent minor python 3 versions
RUN apt-get update --yes \
    && apt-get install --yes software-properties-common \
    && add-apt-repository --yes ppa:deadsnakes/ppa \
    && apt-get update --yes \
    && apt-get install --yes python3.6 python3.7 python3.8 python3.9 python3.10 \
    && apt install --yes python3-pip \
    && pip3 install tox

WORKDIR /app

COPY ./flask_opensearch/ ./
COPY ./tests ./
COPY ./README.md ./
COPY setup.py ./
COPY setup.cfg ./
COPY tox.ini ./

ENTRYPOINT ["tox"]
