from subprocess import check_output, DEVNULL, PIPE
from tqdm import trange, tqdm
import random

def brute(passphrase):
    # gpg --batch --yes --passphrase x --output message.txt --decrypt message.txt.gpg
    cmd = ['gpg', '-v', '--pinentry-mode=loopback', '--passphrase', passphrase, '--output', 'message.txt', '--decrypt', 'message.txt.gpg']

    try:
        # ignore stderr and stdout
        check_output(cmd, stderr=PIPE)
        print(f"Passphrase found: {passphrase}")
        return True
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"Passphrase {passphrase} failed: {e}")
        return False


data = '''646-779-3994
347-416-6565
718-500-3047
718-557-9611
718-808-8484
646-779-9417
718-407-5159
718-222-2506
718-407-5159
718-222-2500'''.split('\n')

print(len(data))
for line in tqdm(data):
    num = line.replace('-', '')
    print(brute(num))