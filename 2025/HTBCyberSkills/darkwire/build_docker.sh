#!/bin/bash
docker build -t darkwire .
docker run  --name=darkwire --rm -p 1337:1337 -it darkwire