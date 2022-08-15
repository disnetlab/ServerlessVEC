import requests
from PIL import Image
import json
import base64
from io import BytesIO
import sys


img = Image.open("testImg.jpg")

#Convert Pillow Image to bytes and then to base64
buffered = BytesIO()
img.save(buffered, format="JPEG")
img_byte = buffered.getvalue() # bytes
img_base64 = base64.b64encode(img_byte) #Base64-encoded bytes * not str

#It's still bytes so json.Convert to str to dumps(Because the json element does not support bytes type)
img_str = img_base64.decode('utf-8') # str

files = {
    "text":"hogehoge",
    "img":img_str
    }

r = requests.post("http://"+sys.argv[1]+":"+sys.argv[2], json=json.dumps(files)) #POST to server as json

print(r.json())
