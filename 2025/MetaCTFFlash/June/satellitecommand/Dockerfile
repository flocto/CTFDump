FROM redpwn/jail

COPY --from=alpine / /srv
RUN mkdir /srv/app

COPY ./challenge /srv/app/run
COPY ./flag.txt /srv/app/flag.txt

# Create satellite-themed directory structure
RUN mkdir -p /srv/app/satellite/systems && \
    mkdir -p /srv/app/satellite/telemetry && \
    mkdir -p /srv/app/satellite/comms && \
    mkdir -p /srv/app/satellite/payload && \
    mkdir -p /srv/app/satellite/maintenance

# Create some interesting files
RUN echo "POWER_LEVEL=98.2%" > /srv/app/satellite/systems/power.dat && \
    echo "Last maintenance performed: 2025-06-06\nNext scheduled: 2025-07-01" > /srv/app/satellite/maintenance/schedule.log && \
    echo "ENCRYPTED COMMS ACTIVE\nFREQUENCY: 137.5 MHz\nMODULATION: QPSK" > /srv/app/satellite/comms/radio.conf && \
    echo "Temperature: 23.5°C\nAltitude: 408.2 km\nVelocity: 7.66 km/s" > /srv/app/satellite/telemetry/status.dat && \
    echo "=== CUI ===\nThis file contains sensitive mission data.\nRead access denied." > /srv/app/satellite/payload/mission.dat && \
    echo "=== SYSTEM LOGS ===\n[WARNING] Unauthorized access attempt from 192.168.1.100\n[INFO] Orbital correction complete\n[ERROR] Failed to validate security token" > /srv/app/satellite/systems/system.log

RUN chmod 755 /srv/app/run
RUN chmod 444 /srv/app/flag.txt
# Set permissions for satellite directories
RUN chmod -R 755 /srv/app/satellite

ENV JAIL_MEM=50M
ENV JAIL_TIME=60

ENV JAIL_PORT=1337
ENV JAIL_CONNS_PER_IP=5
ENV JAIL_MAX_CONNS=50
