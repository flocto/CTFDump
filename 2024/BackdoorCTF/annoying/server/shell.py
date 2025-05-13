#!/usr/bin/python3
import secrets
import hashlib
from subprocess import Popen, PIPE
from threading import Timer
import docker
from docker.types import Mount
import sys
import time


# 22
# copied from: https://github.com/balsn/proof-of-work
class NcPowser:
    def __init__(self, difficulty=23, prefix_length=16):
        self.difficulty = difficulty
        self.prefix_length = prefix_length

    def get_challenge(self):
        return secrets.token_urlsafe(self.prefix_length)[:self.prefix_length].replace('-', 'b').replace('_', 'a')

    def verify_hash(self, prefix, answer):
        h = hashlib.sha256()
        h.update((prefix + answer).encode())
        bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
        return bits.startswith('0' * self.difficulty)
    

# Credits: ChatGPT
def run_docker_container_with_timeout(upload_path, timeout_seconds):
    client = docker.from_env()

    # Define container options
    container_options = {
        "image": "annoying-chall",
        "stdin_open": True,
        "command": "/bin/bash",
        "mem_limit": "4096m",
        "network": "none",
        "auto_remove": True,
        "mounts": [
        Mount(target="/player", source=upload_path, type="bind", read_only=True)
        ],
        "devices": ["/dev/kvm:/dev/kvm:rwm"]
    }

    # Create and start the container
    container = client.containers.run(**container_options, detach=True)
    container_id = container.id
    time.sleep(1)
    proc = Popen(["docker", "exec", "-i", container_id, "/run.sh"])
    # Function to stop the container if it runs for too long
    timer = Timer(timeout_seconds, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
    finally:
        print("[*] time's up...")
        print("[*] exiting....")
        timer.cancel()
        container.stop()
        container.remove()
        # Return the container's exit code and output
    return container


if __name__ == '__main__':
    powser = NcPowser()
    prefix = powser.get_challenge()
    print(f"[*] please solve: sha256({prefix} + ???) == {'0'*powser.difficulty}({powser.difficulty})... ")
    print(f"[*] prefix: {prefix}")
    print(f"[*] difficulty: {powser.difficulty}")
    sys.stdout.flush()
    answer = input(" >")    
    if not powser.verify_hash(prefix, answer):
        print(f"[*] incorrect..")
        exit(0)
    print(f"[*] correct, starting up")
    print("[*] Give me the right password...")
    pswd = input(" >")
    if pswd == "**REDACTED**":
        flag_str = "**REDACTED**"
        print("flag{"+flag_str+"}")
    exit(0)
