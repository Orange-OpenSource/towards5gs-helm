FROM ueransim-base AS builder
FROM ubuntu:20.04

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install iproute2 traceroute curl iputils-ping dnsutils

WORKDIR /ueransim

RUN mkdir config build

COPY --from=builder /ueransim/build/nr-ue ./build/
COPY --from=builder /ueransim/build/nr-cli ./build/
COPY --from=builder /ueransim/build/nr-binder ./build/
COPY --from=builder /ueransim/build/libdevbnd.so ./build/
COPY --from=builder /ueransim/config/* ./config/

VOLUME [ "/ueransim/config" ]

WORKDIR /ueransim/build

COPY wrapper.sh wrapper.sh
RUN chmod +x wrapper.sh

#ENTRYPOINT ["./wrapper.sh"]
