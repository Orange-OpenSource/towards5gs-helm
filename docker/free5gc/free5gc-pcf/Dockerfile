FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

WORKDIR /free5gc
RUN mkdir -p config/ log/ cert/ pcf/

# Copy executable and default certs
COPY --from=builder /free5gc/pcf ./pcf
COPY --from=builder /free5gc/cert/pcf.pem ./cert/
COPY --from=builder /free5gc/cert/pcf.key ./cert/
COPY --from=builder /free5gc/config/pcfcfg.yaml ./config/

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/config/TLS" ]

WORKDIR /free5gc/pcf

