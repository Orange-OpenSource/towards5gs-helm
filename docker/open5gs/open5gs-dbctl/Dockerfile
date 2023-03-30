FROM open5gs-base AS base
FROM bitnami/mongodb:4.4.4-debian-10-r0

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

WORKDIR /open5gs

# Copy webui folder
COPY --from=base /open5gs/misc/db/open5gs-dbctl ./






