#! /bin/sh
#
docker build -t multi-target .
docker run -it --rm -p 1341:1341 -p 12345:12345 multi-target
