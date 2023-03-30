FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

WORKDIR /free5gc
RUN mkdir -p config/ log/ config/TLS/ udr/

# Copy executable and default certs
COPY --from=builder /free5gc/udr ./udr
COPY --from=builder /free5gc/config/TLS/udr.pem ./config/TLS/
COPY --from=builder /free5gc/config/TLS/udr.key ./config/TLS/
COPY --from=builder /free5gc/config/udrcfg.yaml ./config/

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/config/TLS" ]

WORKDIR /free5gc/udr

