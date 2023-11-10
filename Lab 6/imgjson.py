import json
import base64
data = {}
with open('tarotimg/compressresult.jpg', mode='rb') as file:
    img = file.read()

data['img'] = base64.b64encode(img).decode('utf-8')
# print(json.dumps(data))
print(str(json.dumps(data)))
print("img to json")