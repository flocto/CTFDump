# Stage 1: Build the minimal environment
FROM ubuntu:20.04 AS base

# Install only what’s necessary
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    jq \
    coreutils && \
    rm -rf /var/lib/apt/lists/*

# Create restricted bin
RUN mkdir -p /restricted-bin && \
    cp /bin/ls /restricted-bin/ && \
    cp /bin/cat /restricted-bin/
                
# Create user and home
RUN useradd -ms /bin/rbash ctfuser
WORKDIR /home/ctfuser

# Copy the challenge files
COPY challenge.sh /home/ctfuser/challenge_script.sh
COPY whitelist.json /app/whitelist.json

# Permissions and restricted profile
RUN echo 'export PATH=/restricted-bin' >> /home/ctfuser/.bash_profile && \
    chmod +x /home/ctfuser/challenge_script.sh

# Stage 2: Final jail
FROM pwn.red/jail

# Copy the entire restricted environment
COPY --from=base / /srv

# redpwn/jail expects a /srv/app/run entrypoint
COPY --from=base /home/ctfuser/challenge_script.sh /srv/app/run

# Make sure /srv/app/run is executable
RUN chmod +x /srv/app/run

ENV JAIL_TIME 120
ENV JAIL_CONNS_PER_IP 5
ENV JAIL_MEM 20M
ENV JAIL_TMP_SIZE 20M
