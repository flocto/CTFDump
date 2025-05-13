import zipfile

password = b'Coq\\IP1o7hr#yyW7'  # Make sure the password is in bytes
zipf = "rabbit.zip"

with zipfile.ZipFile(zipf, 'r') as zip_ref:
    for file in zip_ref.namelist():
        try:
            with zip_ref.open(file, pwd=password) as f:
                print(file, f.read())
        except:
            pass
