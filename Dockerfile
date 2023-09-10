FROM alpine:latest
MAINTAINER Narasimhan M.G. github.com/Naras 
RUN apk add --update python3 python3-dev \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --upgrade pip setuptools
COPY ./Amarakosha.db /usr/local/Amarakosha/Amarakosha.db
COPY ./Bandarkar.txt /usr/local/Amarakosha/Bandarkar.txt
COPY ./source/Controller /usr/local/Amarakosha/source/Controller
COPY ./source/Model /usr/local/Amarakosha/source/Model
COPY  ./requirements_rest_docker.txt /usr/local/Amarakosha/requirements.txt
EXPOSE 5002
WORKDIR /usr/local/Amarakosha/
RUN pip3 install -r requirements.txt
CMD python3 source/Controller/restService.py
