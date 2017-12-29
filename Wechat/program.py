import os

import cv2
import itchat
import math
import pandas as pd
import re

from PIL import Image

from Wechat.add_chrismas_hat import AddHat


def __LoginAndGetFriends():
  itchat.auto_login()
  return itchat.get_friends(update=True)


def GetSex(sex):
  if sex == 1:
    return "Male"
  elif sex == 2:
    return 'Female'
  else:
    return 'Other'


def __DumpFriends(friends, data_dir):
  features = []
  for f in friends:
    feature = {
      'UserName': f['UserName'],
      'NickName': f['NickName'],
      'Sex': GetSex(f['Sex']),
      'City': f['City'],
      'Province': f['Province'],
      'Signature': f['Signature']
    }
    features.append(feature)
  df = pd.DataFrame(features)
  df.index.names = ['Num']
  df.to_csv(os.path.join(data_dir, 'friends.csv'))
  return df


def __DumpHeadImg(friends, data_dir):
  num = 1
  for friend in friends:
    with open(os.path.join(data_dir, 'photo_wall_' + str(num) + '.jpg'), 'wb') as output:
      num += 1
      img = itchat.get_head_img(userName=friend['UserName'])
      output.write(img)

def __AddHat(data_dir):
  hat_img = cv2.imread(os.path.join('data', 'hat.png'), -1)

  p = re.compile('photo_wall_[0-9]+.jpg')
  for file in os.listdir(data_dir):
    if not p.match(file):
      continue
    print('processing ', file)
    face_img = cv2.imread(os.path.join(data_dir, file))
    add_hat, added = AddHat(face_img, hat_img)
    if added:
      cv2.imwrite(os.path.join(data_dir, 'hat_' + file), add_hat)

def __GeneratePhotoWall(data_dir, pre_fix, output_name):
  p = re.compile(pre_fix + '[0-9]+.jpg')
  count = 0
  for file in os.listdir(data_dir):
    if p.match(file):
      count += 1
  each_size = int(math.sqrt(float(640 * 640) / count))

  x, y = 0, 0
  image = Image.new('RGBA', (640, 640))

  for file in os.listdir(data_dir):
    if not p.match(file):
      continue

    try:
      cur_img = Image.open(os.path.join(data_dir, file))
    except IOError:
      print('Error processing {}'.format(file))
      continue
    cur_img = cur_img.resize((each_size, each_size), Image.ANTIALIAS)
    image.paste(cur_img, (x * each_size, y * each_size))
    x += 1
    if x == int(640 / each_size):
      x = 0
      y += 1

  image.save(os.path.join(data_dir, output_name))
  itchat.send_image(os.path.join(data_dir, output_name), 'filehelper')

def run():
  friends = __LoginAndGetFriends()

  data_dir = ''.join(filter(str.isalpha, friends[0]['NickName']))
  if len(data_dir) == 0:
    data_dir = friends[0]['NickName']
  if not os.path.exists(data_dir):
    os.mkdir(data_dir)

  __DumpFriends(friends, data_dir)
  __DumpHeadImg(friends, data_dir)
  __GeneratePhotoWall(data_dir, 'photo_wall_', 'photo_wall.png')
  __AddHat(data_dir)
  __GeneratePhotoWall(data_dir, 'hat_photo_wall', 'hat_photo_wall.png')


if __name__ == '__main__':
  run()
