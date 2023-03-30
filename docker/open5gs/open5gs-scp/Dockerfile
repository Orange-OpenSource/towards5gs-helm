FROM open5gs-base AS builder
FROM alpine:3.13

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

WORKDIR /open5gs

RUN mkdir -p install/bin install/lib install/etc

# Copy executable, config, certificates and libs
COPY --from=builder /open5gs/install/bin/open5gs-scpd ./install/bin/
COPY --from=builder /open5gs/install/etc/open5gs/scp.yaml ./install/etc/
COPY --from=builder /open5gs/install/etc/open5gs/tls/scp* ./install/tls/
COPY --from=builder /open5gs/install/etc/open5gs/tls/ca* ./install/tls/
COPY --from=builder /open5gs/install/lib/scp-libs/* /usr/local/lib/

RUN ldconfig /open5gs/install/bin/open5gs-scpd

VOLUME [ "/open5gs/install/etc" ]

WORKDIR /open5gs/install/bin
