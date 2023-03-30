FROM open5gs-base AS builder
FROM alpine:3.13

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

WORKDIR /open5gs

RUN mkdir -p install/bin install/lib install/etc

# Copy executable, config, certificates and libs
COPY --from=builder /open5gs/install/bin/open5gs-amfd ./install/bin/
COPY --from=builder /open5gs/install/etc/open5gs/amf.yaml ./install/etc/
COPY --from=builder /open5gs/install/etc/open5gs/tls/amf* ./install/tls/
COPY --from=builder /open5gs/install/etc/open5gs/tls/ca* ./install/tls/
COPY --from=builder /open5gs/install/lib/amf-libs/* /usr/local/lib/

RUN ldconfig /open5gs/install/bin/open5gs-amfd

VOLUME [ "/open5gs/install/etc" ]

WORKDIR /open5gs/install/bin
