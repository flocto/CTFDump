FROM cybersecnatlab/challenge-jail:ubuntu-noble@sha256:94d94b54986f4a49b03f258a2effe64611a170312bda62dcd63b8197f58621ec

RUN apt install python3 python3-pip ffmpeg libsm6 libxext6 gfortran libzbar-dev -y

RUN pip3 install pyzbar opencv-python pillow --break-system-packages