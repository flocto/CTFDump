from concurrent.futures import ProcessPoolExecutor, as_completed
from subprocess import check_output, DEVNULL
from tqdm import tqdm

def brute(passphrase):
    # gpg --batch --yes --passphrase x --output message.txt --decrypt message.txt.gpg
    cmd = ['gpg', '--batch', '--yes', '--passphrase', passphrase, '--output', 'message.txt', '--decrypt', 'message.txt.gpg']

    try:
        # ignore stderr and stdout
        check_output(cmd, stderr=DEVNULL)
        return passphrase  # return the correct passphrase if found
    except:
        return None  # return None if the passphrase is wrong

def brute_force_parallel(start, end):
    for i in range(start, end):
        phone = str(i).zfill(7)
        if brute(phone):
            return phone  # return the correct passphrase if found
    return None

def main():
    num_workers = 4  # Set the number of workers (adjust based on your CPU)
    total_range = 10000000
    chunk_size = total_range // num_workers
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(brute_force_parallel, i * chunk_size, (i + 1) * chunk_size)
            for i in range(num_workers)
        ]

        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"Passphrase found: {result}")
                executor.shutdown(wait=False)  # Stop other workers
                break
        else:
            print("No passphrase found")

if __name__ == "__main__":
    main()