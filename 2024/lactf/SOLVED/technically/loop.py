import subprocess
import os
import signal

data = open('technically_correct', 'rb').read()
BYTES = range(0x0, len(data))

for i in BYTES:
    print(f"Trying {i:x}")
    # if i == 618: break
    patched = bytearray(data)
    patched[i:i+2] = b'\xeb\xfc' # infinite loop
    print(data[i:i+2])
    with open('technically_correct_patched2', 'wb') as f:
        f.write(patched)
        f.close()
    
    try:
        proc = subprocess.Popen(['./technically_correct_patched2', 'XXXX'])
        proc.wait(1)
        # check if the process is still running
        pid = proc.pid
        if os.path.exists(f"/proc/{pid}"):
            print(f"Process {pid} is still running")
            os.killpg(os.getpgid(pid), signal.SIGTERM)
            input()

        else: # print error code
            print(f"Error code: {proc.returncode}")
            proc.kill()
    except Exception as e:
        print(f"Error: {e}")