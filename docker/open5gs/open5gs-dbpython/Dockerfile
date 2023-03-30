FROM open5gs-base AS base
FROM alpine:3.12

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

RUN apk --no-cache add python3 py3-pip && ln -s $(which python3) /usr/bin/python
RUN pip install pymongo bson

WORKDIR /open5gs

COPY --from=base /open5gs/misc/db/python/* ./
COPY add_subscribers.py add_subscribers.py
