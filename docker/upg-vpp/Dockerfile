FROM ubuntu:18.04 AS builder

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y sudo git make

WORKDIR /
RUN git clone -b stable/1.2 https://github.com/travelping/upg-vpp.git
WORKDIR /upg-vpp

RUN git config --global user.email "khich.abderaouf@gmail.com"
RUN git config --global user.name "raoufkh"

RUN make update-vpp

RUN echo "APT::Get::Assume-Yes "true";" >> /etc/apt/apt.conf.d/90forceyes && \
    echo "APT::Get::force-yes "true";" >> /etc/apt/apt.conf.d/90forceyes

RUN apt-get update
WORKDIR /upg-vpp/vpp
RUN make install-dep && \
    make install-ext-deps && \
    make build-release


FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

RUN apt-get update
RUN apt-get install -y libssl-dev openssl libcurl4-openssl-dev libnuma1 libhyperscan-dev

WORKDIR /upg-vpp/bin
COPY --from=builder /upg-vpp/vpp/build-root/install-vpp-native/vpp/bin/vpp .
COPY --from=builder /upg-vpp/vpp/build-root/install-vpp-native/vpp/bin/vppctl .

WORKDIR /usr/local/lib
COPY --from=builder /upg-vpp/vpp/build-root/install-vpp-native/vpp/lib/ .

RUN ldconfig

VOLUME [ "/upg-vpp/etc" ]

RUN groupadd vpp

WORKDIR /upg-vpp/bin

