FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

WORKDIR /free5gc
RUN mkdir -p log/ config/ TLS/ amf/

# Copy executable and default certs/configs
COPY --from=builder /free5gc/amf ./amf
COPY --from=builder /free5gc/config/TLS/amf.pem ./config/TLS/
COPY --from=builder /free5gc/config/TLS/amf.key ./config/TLS/
COPY --from=builder /free5gc/config/amfcfg.yaml ./config/

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/config/TLS" ]

WORKDIR /free5gc/amf

