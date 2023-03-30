FROM alpine:3.12

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

RUN apk --no-cache add python3 py3-pip && ln -s $(which python3) /usr/bin/python
RUN pip install pymongo bson

WORKDIR /free5gc

COPY free5gc_db.py .
COPY add_subscribers.py add_subscribers.py
