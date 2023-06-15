FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

# Install N3IWF dependencies
RUN apk add -U iproute2

WORKDIR /free5gc
RUN mkdir -p log/ cert/ n3iwf/

# Copy executable and default certs/configs
COPY --from=builder /free5gc/n3iwf ./n3iwf
COPY --from=builder /free5gc/cert/n3iwf.pem ./cert/
COPY --from=builder /free5gc/cert/n3iwf.key ./cert/
COPY --from=builder /free5gc/config/n3iwfcfg.yaml ./config/

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/config/TLS" ]

WORKDIR /free5gc/n3iwf
