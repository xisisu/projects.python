# https://www.youtube.com/watch?v=UtNYzv8gLbs

import json
import os
import random
import string

import requests

random.seed = (os.urandom(1024))
chars = string.ascii_letters + string.digits

url = 'http://fake.url.list'

names = json.loads(open('name.json', 'r').read())

for name in names:
  name_extra = ''.join(random.choice(string.digits))
  username = name.lower() + name_extra + '@gmail.com'
  password = ''.join(random.choice(chars) for i in range(10))

  requests.post(url, allow_redirects=False, data={
    'user': username,
    'pwd': password
  })

  print(username, password)
