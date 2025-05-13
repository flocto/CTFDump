FROM ocaml/opam:debian-ocaml-4.14


RUN sudo apt-get update && sudo apt-get install -y \
    curl \
    git \
    gnupg \
    software-properties-common \
    build-essential \
    wget \
    m4 \
    unzip \
    zlib1g-dev \
    libgmp-dev \
    libssl-dev \
    ghc

RUN opam init -a -y && eval $(opam env) && opam install -y ocamlformat dune 

RUN sudo apt-get update && \
        sudo apt-get -y upgrade && \
        sudo apt-get install -y xinetd iproute2 libc++1

COPY --chown=root:opam ./build/ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:opam ./build/start.sh /home/user/start.sh

RUN wget https://github.com/FStarLang/FStar/releases/download/v2024.12.03/fstar_2024.12.03_Linux_x86_64.tar.gz && tar xf fstar_2024.12.03_Linux_x86_64.tar.gz
ENV PATH="/home/opam/fstar/bin:$PATH"

ADD --chown=opam:opam src /home/opam/src
WORKDIR src
RUN eval $(opam env) && opam install --deps-only .
RUN eval $(opam env) && dune build
WORKDIR /home/opam
RUN cp ./src/_build/default/bin/main.exe chall && rm -rf src

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]

