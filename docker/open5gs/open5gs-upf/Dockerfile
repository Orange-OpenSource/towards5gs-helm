FROM open5gs-base AS builder
FROM alpine:3.13

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

# Install dependencies
RUN apk --no-cache add iproute2 iptables

WORKDIR /open5gs

RUN mkdir -p install/bin install/lib install/etc

# Copy executable, config, and libs
COPY --from=builder /open5gs/install/bin/open5gs-upfd ./install/bin/
COPY --from=builder /open5gs/install/etc/open5gs/upf.yaml ./install/etc/
COPY --from=builder /open5gs/install/lib/upf-libs/* /usr/local/lib/

RUN ldconfig /open5gs/install/bin/open5gs-upfd

VOLUME [ "/open5gs/install/etc" ]

WORKDIR /open5gs/install/bin
