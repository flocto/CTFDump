import re
import subprocess
pid = 78315

# blocks
# 1bd4eff000-1bd4f00000

maps_file = open(f'/proc/{pid}/maps', 'r')
output_file = open("dump.bin", 'wb')
out_buf = bytearray(0x1000 * 64)
for i, line in enumerate(maps_file.readlines()[:-3]):
    startend, perms, offset, *_ = re.split(r'[ ]', line)
    start, end = startend.split('-')
    start = int(start, 16)
    end = int(end, 16)
    offset = int(offset, 16)

    try:
        subprocess.check_output(['dd', f'if=/proc/{pid}/mem', f'of=dump.tmp', f'bs=1', f'skip={start}', f'count={end-start}'])

        tmp_data = open('dump.tmp', 'rb').read()
        out_buf[offset:offset+len(tmp_data)] = tmp_data
    except Exception as e:
        print(f"Error: {e}")

output_file.write(out_buf.strip(b'\x00'))