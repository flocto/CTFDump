FROM ubuntu:24.04

RUN apt-get update && apt-get install -y qemu-system-x86 qemu-utils gdb

WORKDIR /app

COPY . /app

ENTRYPOINT ["/bin/bash"]