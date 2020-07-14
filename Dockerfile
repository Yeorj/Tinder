ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION-alpine

RUN apk add build-base
RUN apk add bash
RUN apk add libxml2-dev libxslt-dev
RUN apk add protoc

# Upgrade pip
RUN pip3 install --upgrade pip

# Create a directory for the app code
WORKDIR /app

ADD protobuf protobuf
ADD tinder_api tinder_api
ADD README.md .
ADD setup.py .

RUN python3 setup.py install

RUN rm -rf ./protobuf ./tinder_api README.md setup.py

ADD tests tests

