FROM ueransim-base AS builder
FROM ubuntu:20.04

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install libsctp-dev lksctp-tools dnsutils

WORKDIR /ueransim

RUN mkdir config build

# Copy binaries
COPY --from=builder /ueransim/build/nr-gnb ./build/
COPY --from=builder /ueransim/build/nr-cli ./build/
COPY --from=builder /ueransim/config/* ./config/

VOLUME [ "/ueransim/config" ]

WORKDIR /ueransim/build

#ENTRYPOINT ["./nr-gnb", "-c", "../config/free5gc-gnb.yaml"]
