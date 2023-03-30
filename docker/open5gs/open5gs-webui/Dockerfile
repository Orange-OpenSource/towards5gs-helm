FROM open5gs-base AS base
FROM node:lts

LABEL maintainer="raoufkh <khichane.araouf@gmail.com>"

WORKDIR /

# Copy webui folder
COPY --from=base /open5gs/webui ./webui
#RUN git clone -b v2.4.3 https://github.com/open5gs/open5gs

# Build the WEBUI
WORKDIR /webui
RUN npm install && \
    npm run build
#RUN npm ci --no-optional

CMD npm run dev
