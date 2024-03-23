ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-alpine as host-a

WORKDIR /host

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT /bin/sh

