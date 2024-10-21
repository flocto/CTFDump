#!/usr/bin/python3
import subprocess
from tempfile import TemporaryDirectory
import os
from PIL import Image
import base64
import cv2
from pyzbar.pyzbar import decode

encoded_file = input("Please provide your .t file base64-encoded: ")

data = base64.b64decode(encoded_file)

with TemporaryDirectory() as tempdir:
    with open(f"{tempdir}/data.t", "wb") as f:
        f.write(data)
    subprocess.check_output(["./printer", f"{tempdir}/data.t"])
    if(not os.path.exists(f"{tempdir}/data.t.ppm")):
        print("Error in printer")
        exit(-1)
    # print(open(f"{tempdir}/data.t.ppm", "rb").read()[:8])
    image = Image.open(f"{tempdir}/data.t.ppm")
    # debug
    image.save('./data.png')
    image.save('./data.ppm')
    image.save(f"{tempdir}/data.t.png")
    image = cv2.imread(f"{tempdir}/data.t.png")
    decoded_text = decode(image)
    if(len(decoded_text)>0):
        data = decoded_text[0].data
        if(data==b"WA33INAR7JDKUPNJ"):
            flag = os.getenv("FLAG")
            if(flag is None):
                print("Flag not found on server. Please contact an admin.")
            else:
                print(flag)
    else:
        print("Nope")