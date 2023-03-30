FROM free5gc-base AS builder
FROM alpine:3.13.6

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

ENV GIN_MODE="release"

RUN apk --no-cache add libc6-compat

WORKDIR /free5gc
RUN mkdir -p config/ webconsole/public

# Copy executable and default configs/statics
COPY --from=builder /free5gc/webconsole ./webconsole/
COPY --from=builder /free5gc/config/webuicfg.yaml ./config/
COPY --from=builder /free5gc/public ./webconsole/public

VOLUME [ "/free5gc/config" ]
#VOLUME [ "/free5gc/support/TLS" ]

WORKDIR /free5gc/webconsole

