FROM python:3.11.7-slim

RUN apt-get update && apt-get install -y curl git socat && rm -rf /var/lib/apt/lists/*

RUN true && \
    apt-get update && \
    apt-get install -y curl git socat bsdmainutils && \
    rm -rf /var/cache/apt/lists /var/lib/apt/lists/* && \
    true

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /home/ctf

ENV FOUNDRY_DIR=/opt/foundry
ENV PATH=${FOUNDRY_DIR}/bin/:${PATH}
RUN true && \
    curl -L https://foundry.paradigm.xyz | bash && \
    foundryup && \
    true

COPY . .

RUN cd /home/ctf/challenge/project && forge build --out /artifacts/out --cache-path /artifacts/cache

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*