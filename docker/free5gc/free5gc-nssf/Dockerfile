FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

WORKDIR /free5gc
RUN mkdir -p log/ config/TLS/ nssf/

# Copy executable and default certs
COPY --from=builder /free5gc/nssf ./nssf
COPY --from=builder /free5gc/config/TLS/nssf.pem ./config/TLS/
COPY --from=builder /free5gc/config/TLS/nssf.key ./config/TLS/
COPY --from=builder /free5gc/config/nssfcfg.yaml ./config/

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/config/TLS" ]

WORKDIR /free5gc/nssf

