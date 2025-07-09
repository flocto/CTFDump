FROM python:3

WORKDIR /

COPY stretch buster bullseye bookworm main.py flag.txt test.py test.svg /
RUN pip install Pillow

# mount /dump as ./dump
VOLUME ["/dump"]

# CMD ["python", "main.py"]
ENTRYPOINT ["/bin/bash"]