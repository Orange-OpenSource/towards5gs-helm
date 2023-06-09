FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

WORKDIR /free5gc
RUN mkdir -p log/ cert/ smf/

# Copy executable and default certs
COPY --from=builder /free5gc/smf ./smf
COPY --from=builder /free5gc/cert/smf.pem ./cert/
COPY --from=builder /free5gc/cert/smf.key ./cert/
COPY --from=builder /free5gc/config/smfcfg.yaml ./config/
COPY --from=builder /free5gc/config/uerouting.yaml ./config/

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/config/TLS" ]

WORKDIR /free5gc/smf
