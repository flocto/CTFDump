import random
import threading
from queue import Queue
import dns.resolver
import dns.rdatatype

NUM_THREADS = 10
MAX_NUMBER = 10_000_000
MAX_NUMBER = 100

dns_server = "34.169.35.135"

def worker(queue):
    dns_query = dns.resolver.Resolver()
    dns_query.nameservers = [dns_server]
    while not queue.empty():
        if queue.qsize() % 100 == 0:
            print(f"Remaining: {queue.qsize()}")
        number = queue.get()
        domain = f"{number}.rev.lac.tf"
        def inner():
            try:
                txt_records = dns_query.resolve(domain, dns.rdatatype.TXT)
                # if txt_records:
                #     print(f"TXT record for {domain}:", txt_records.response.answer[0].to_text())
                # if len(txt_records) > 0:
                    # print(f"TXT record for {domain}:", txt_records[0].to_text())
                for record in txt_records:
                    print(f"{domain},{record}")
                    # if ',' in f'{record}':
                    #     open('dump.txt', 'a').write(f"{domain},{record}\n")
                    # # print(domain, record)
                    # open('seen.txt', 'a').write(f"{domain},{record}\n")
            except Exception as e:
                if 'resolution lifetime expired' in str(e):
                    inner()
        inner()
        queue.task_done()

def main():
    queue = Queue()
    rand = list(range(MAX_NUMBER))
    # random.shuffle(rand)

    # seen = open('seen.txt', 'r').read().splitlines()
    # seen = [int(x.split(',')[0].split('.')[0]) for x in seen]
    for i in rand:
        # if i not in seen:
            queue.put(i)

    print(f"Starting {NUM_THREADS} threads")

    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(queue,))
        thread.start()
        threads.append(thread)

    queue.join()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()