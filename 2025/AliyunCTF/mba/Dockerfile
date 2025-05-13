FROM python:bookworm

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git cmake build-essential xinetd
RUN pip3 install lark

WORKDIR /root
RUN git clone https://github.com/Z3Prover/z3
ADD patches/new-tactic.patch /root

WORKDIR /root/z3
RUN git checkout 814d7f4d
RUN git apply /root/new-tactic.patch
RUN mkdir build && cd build && cmake \
  -G "Unix Makefiles" \
  -DCMAKE_BUILD_TYPE=Release \
  -DZ3_BUILD_TEST_EXECUTABLES=OFF \
  -DZ3_INSTALL_PYTHON_BINDINGS=ON \
  -DZ3_BUILD_PYTHON_BINDINGS=ON \
  ..
RUN cd build && make -j && make install

ADD src/server.py /root/
ADD ./problem /etc/xinetd.d/
ADD ./run.sh /root/
RUN chmod +x /root/server.py /root/run.sh

EXPOSE 9048
# CMD ["/root/run.sh"]
CMD ["/usr/sbin/xinetd", "-dontfork"]
