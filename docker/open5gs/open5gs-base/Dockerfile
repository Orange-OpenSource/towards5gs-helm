FROM alpine:3.13

# Install dependencies
RUN apk update
RUN apk --no-cache add \
        alpine-sdk \
        bison flex git cmake meson bash sudo linux-headers bsd-compat-headers yaml-dev lksctp-tools-dev gnutls-dev libgcrypt-dev libidn-dev mongo-c-driver-dev libmicrohttpd-dev curl-dev nghttp2-dev talloc-dev
RUN apk --no-cache add nodejs npm

# Get Open5GS source code
WORKDIR /
RUN git clone -b v2.6.1 https://github.com/open5gs/open5gs && cd open5gs

# Build Open5GS NFs
WORKDIR /open5gs
RUN meson build --prefix=`pwd`/install && \
    ninja -C build && \
    cd build && ninja install

# Copy shared libraries
ENV NF_LIST amf ausf bsf nrf nssf pcf scp smf udm udr upf
WORKDIR /open5gs/install
COPY copy-dependencies.sh .
RUN cp lib64/* lib/ && \
    for NF in ${NF_LIST}; \
        do ./copy-dependencies.sh bin/open5gs-${NF}d lib/${NF}-libs/; done
