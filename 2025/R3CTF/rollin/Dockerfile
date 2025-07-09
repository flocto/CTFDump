FROM ubuntu:24.04

ENV FLAG="R3CTF{not_a_real_flag}"

RUN apt-get update && apt-get install -y gdb gdbserver gcc libc6-dev

RUN useradd -m ctf

WORKDIR /app

COPY ./main .

RUN chmod 755 ./main

EXPOSE 5000
EXPOSE 7777

# CMD ["socat", "-T120", "TCP-LISTEN:5000,reuseaddr,fork,su=ctf", "EXEC:/app/main,pty,echo=0,rawer"]

ENTRYPOINT ["/bin/bash"]
