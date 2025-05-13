import random
import threading
from queue import Queue
import dns.resolver
import dns.rdatatype

NUM_THREADS = 10
MAX_NUMBER = 10_000_000
MAX_NUMBER = 100

dns_server = "34.169.35.135"
dns_query = dns.resolver.Resolver()

def worker(number):
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

def main():
    for i in range(MAX_NUMBER)

if __name__ == "__main__":
    main()