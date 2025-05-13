FROM python:3.10-slim-bookworm@sha256:65c843653048a3ba22c8d5083a022f44aef774974f0f7f70cbf8cee4e931ac96  AS app

# FROM pwn.red/jail

# COPY --from=app / /srv

# COPY chal.py /srv/app/run
# COPY flag.txt /srv/app/flag.txt

# RUN chmod 775 /srv/app/run

# ENV JAIL_TIME=120 JAIL_MEM=10M JAIL_PORT=1337 JAIL_ENV_PYTHONUNBUFFERED=1

COPY test.py /app/test.py
RUN chmod +x /app/test.py

ENTRYPOINT [ "/bin/bash" ]