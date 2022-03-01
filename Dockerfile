FROM ubuntu:18.04

RUN apt-get update --yes \
    && apt-get install --yes software-properties-common \
    && add-apt-repository --yes ppa:deadsnakes/ppa \
    && apt-get update --yes \
    && apt-get install --yes python3.6 python3.7 python3.8 python3.9 \
    && apt install --yes python3-pip \
    && pip3 install tox

WORKDIR /app

COPY ./flask_opensearch/ ./
COPY ./tests ./
COPY ./README.md ./
COPY setup.py ./
COPY setup.cfg ./
COPY tox.ini ./

RUN pip3 install -e .

ENTRYPOINT ["tox"]
