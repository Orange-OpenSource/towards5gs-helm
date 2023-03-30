#FROM bitnami/golang:1.14.4 AS builder
FROM golang:1.14.4-buster AS builder

# Control-plane Supporting Packages
RUN apt-get update
RUN apt-get -y install wget git sudo

# User-plane Supporting Packages
#RUN apt-get update
#RUN apt-get -y install git gcc g++ cmake autoconf libtool pkg-config libmnl-dev libyaml-dev
#RUN go get -u github.com/sirupsen/logrus

# Get Free5GC source code
RUN cd $GOPATH/src \
    && git clone --recursive -b v3.2.1 -j `nproc` https://github.com/free5gc/free5gc.git

# Build all NFs
RUN cd $GOPATH/src/free5gc \
    && make

# Install WebConsole's dependencies
RUN apt remove cmdtest
RUN apt remove yarn
RUN apt-get -y install apt-transport-https
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
RUN apt-get update
RUN apt-get -y install nodejs
RUN apt-get -y install yarn

# Build WebConsole
RUN cd $GOPATH/src/free5gc \
    && make webconsole

# Build the final image
FROM alpine

WORKDIR /free5gc

RUN mkdir -p config/ config/TLS/ public

# Copy executables
COPY --from=builder /go/src/free5gc/bin/* ./
COPY --from=builder /go/src/free5gc/webconsole/bin/webconsole ./

# Copy static files (webui frontend)
COPY --from=builder /go/src/free5gc/webconsole/public ./public

# Copy certificates and config files
COPY --from=builder /go/src/free5gc/config/* ./config/
COPY --from=builder /go/src/free5gc/config/TLS/* ./config/TLS/
