FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

WORKDIR /free5gc
RUN mkdir -p log/ config/TLS/ nrf/

# Copy executable and default certs
COPY --from=builder /free5gc/nrf ./nrf
COPY --from=builder /free5gc/config/TLS/nrf.pem ./config/TLS/
COPY --from=builder /free5gc/config/TLS/nrf.key ./config/TLS/
COPY --from=builder /free5gc/config/nrfcfg.yaml ./config/

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/config/TLS" ]

WORKDIR /free5gc/nrf

