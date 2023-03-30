FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

WORKDIR /free5gc
RUN mkdir -p log/ config/TLS/ udm/

# Copy executable and default certs
COPY --from=builder /free5gc/udm ./udm
COPY --from=builder /free5gc/config/TLS/udm.pem ./config/TLS/
COPY --from=builder /free5gc/config/TLS/udm.key ./config/TLS/
COPY --from=builder /free5gc/config/udmcfg.yaml ./config/

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/config/TLS" ]

WORKDIR /free5gc/udm

