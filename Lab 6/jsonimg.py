import json
import base64
# data = {}
# with open('tarotimg/result.jpg', mode='rb') as file:
#     img = file.read()

# data['img'] = base64.b64encode(img).decode('utf-8')
# print(json.dumps(data))
f = open('img.json')
data = json.load(f)
imgdata = base64.b64decode(data['img'])
filename = 'some_image.jpg'
with open(filename, 'wb') as f:
    f.write(imgdata)