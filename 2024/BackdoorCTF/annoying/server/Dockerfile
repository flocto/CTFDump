FROM ubuntu:24.04
RUN apt-get update -y
RUN apt-get install -y socat python3 python3-pip
RUN curl -sSL https://get.docker.com | sh
RUN apt-get update && apt-get install -y python3-docker
COPY start.sh /
COPY shell.py /
RUN chmod +x /shell.py
EXPOSE 9035
ENTRYPOINT ["/start.sh"]
