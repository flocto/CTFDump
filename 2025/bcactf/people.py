from hashlib import md5
target = '06003dfd18a22e6809e736cf27eaabb6'

username = 'administrator'
emails = [
    'gmail.com',
    'yahoo.com',
    'hotmail.com',
    'outlook.com',
    'icloud.com',
    'aol.com',
    'live.com',
    'mail.com',
    'protonmail.com',
    'yandex.com',
    'duck.com',
]

for email in emails:
    email = f'{username}@{email}'
    hsh = md5(email.encode()).hexdigest()
    if hsh == target:
        print(f'Found email: {email}')
        break