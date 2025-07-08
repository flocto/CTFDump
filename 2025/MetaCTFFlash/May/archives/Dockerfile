FROM ubuntu@sha256:6015f66923d7afbc53558d7ccffd325d43b4e249f41a6e93eef074c9505d2233 AS app

FROM pwn.red/jail@sha256:ee52ad5fd6cfed7fd8ea30b09792a6656045dd015f9bef4edbbfa2c6e672c28c
COPY --from=app / /srv
RUN mkdir /srv/app/
COPY archive /srv/app/run

# Generate a random flag filename at build time
COPY flag.txt /srv/app/flag.txt
RUN DEST="/srv/app/flag_$(head -c 16 /dev/random | md5sum | awk '{print $1}').txt";mv /srv/app/flag.txt $DEST;unset DEST

RUN mkdir -p /srv/app/records
COPY records/* /srv/app/records/
ENV JAIL_TIME=120
ENV JAIL_PORT=1337
ENV JAIL_MEM=100M