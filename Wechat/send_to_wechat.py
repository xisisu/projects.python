import os

import itchat


def run():
  itchat.auto_login()
  # for num in [178, 177, 139, 112, 104, 0]:
  #   file = 'hat_photo_wall_' + str(num) + '.jpg'
  #   itchat.send_image(os.path.join('data', file), 'filehelper')
  itchat.send_image(os.path.join('data/photo_wall.png'), 'filehelper')

if __name__ == '__main__':
  run()
