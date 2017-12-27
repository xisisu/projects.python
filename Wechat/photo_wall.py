import math
import os

import PIL.Image as Image
import itchat


def __GetOutputDir():
  return 'data'


def __ClearImage():
  for file in os.listdir(__GetOutputDir()):
    if file.startswith('photo_wall_'):
      os.remove(file)

def __CheckExistImage():
  for file in os.listdir(__GetOutputDir()):
    if file.startswith('photo_wall_'):
      return True
  return False

def GetFriends():
  itchat.auto_login()
  return itchat.get_friends(update=True)


def SaveFriendsImage(friends=None):
  num = 0
  for friend in friends:
    with open(os.path.join(__GetOutputDir(), 'photo_wall_' + str(num) + '.jpg'), 'wb') as output:
      num += 1
      img = itchat.get_head_img(userName=friend['UserName'])
      output.write(img)


def PlotPhotoWall(send_file = False):
  total_count = len(os.listdir(__GetOutputDir()))
  each_size = int(math.sqrt(float(640 * 640) / total_count))

  x, y = 0, 0
  image = Image.new('RGBA', (640, 640))
  for file in os.listdir(__GetOutputDir()):
    try:
      cur_img = Image.open(os.path.join(__GetOutputDir(), file))
    except IOError:
      print('Error processing {}'.format(file))
      continue
    cur_img = cur_img.resize((each_size, each_size), Image.ANTIALIAS)
    image.paste(cur_img, (x * each_size, y * each_size))
    x += 1
    if x == int(640 / each_size):
      x = 0
      y += 1

  image.save(os.path.join(__GetOutputDir(), 'photo_wall.png'))
  if send_file:
    itchat.send_image(os.path.join(__GetOutputDir(), 'photo_wall.png'), 'filehelper')


def run():
  # __ClearImage()
  if not __CheckExistImage():
    friends = GetFriends()
    SaveFriendsImage(friends)
    PlotPhotoWall(send_file=True)
  PlotPhotoWall(send_file=False)


if __name__ == '__main__':
  run()
