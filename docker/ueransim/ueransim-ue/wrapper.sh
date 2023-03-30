#!/bin/bash

mkdir /dev/net
mknod /dev/net/tun c 10 200
./nr-ue -c ../config/ue-config.yaml
