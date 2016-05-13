FROM python:2-onbuild
WORKDIR /usr/src/app
RUN pip install .
