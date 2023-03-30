FROM open5gs-base AS builder
FROM alpine:3.13

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

WORKDIR /open5gs

RUN mkdir -p install/bin install/lib install/etc

# Copy executable, config, certificates and libs
COPY --from=builder /open5gs/install/bin/open5gs-udmd ./install/bin/
COPY --from=builder /open5gs/install/etc/open5gs/udm.yaml ./install/etc/
COPY --from=builder /open5gs/install/etc/open5gs/hnet/*.key ./install/hnet/
COPY --from=builder /open5gs/install/etc/open5gs/tls/udm* ./install/tls/
COPY --from=builder /open5gs/install/etc/open5gs/tls/ca* ./install/tls/
COPY --from=builder /open5gs/install/lib/udm-libs/* /usr/local/lib/

RUN ldconfig /open5gs/install/bin/open5gs-udmd

VOLUME [ "/open5gs/install/etc" ]

WORKDIR /open5gs/install/bin
