FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

# Install UPF dependencies
RUN apk --no-cache add iproute2 iptables

WORKDIR /free5gc
RUN mkdir -p config/ upf/

# Copy executable and default configs/certs
COPY --from=builder /free5gc/upf ./upf/
COPY --from=builder /free5gc/config/upfcfg.yaml ./config/

VOLUME [ "/free5gc/config" ]

WORKDIR /free5gc/upf
