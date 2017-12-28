# from https://github.com/LiuXiaolong19920720/Add-Christmas-Hat

import os

import cv2
import dlib


def __GetOutput():
  return 'data'


def __ResizeImage(img, width, y):
  resize_hat_height = int(round(img.shape[0] * width / img.shape[1]))
  if resize_hat_height > y:
    resize_hat_height = y - 1
  resize_hat_width = int(round(img.shape[1] * width / img.shape[1]))
  resize = (resize_hat_width, resize_hat_height)
  return cv2.resize(img, resize), resize


def __GetEyeCenter(img, detector, predictor):
  shape = predictor(img, detector)

  left_eye, right_eye = shape.part(0), shape.part(2)
  eye_center = ((left_eye.x + right_eye.x) // 2, (left_eye.y + right_eye.y) // 2)

  return eye_center


def __GetHatArea(img, y, eye_center, resize):
  return img[y - resize[1]:y,
         (eye_center[0] - resize[0] // 3):(eye_center[0] + resize[0] // 3 * 2)]


def __RemoveHatArea(img, mask):
  img = img.astype(float)
  mask = cv2.merge((mask, mask, mask))
  alpha = mask.astype(float) / 255

  alpha = cv2.resize(alpha, (img.shape[1], img.shape[0]))
  bg = cv2.multiply(alpha, img)
  bg = bg.astype('uint8')
  return bg


def __AddHat(img, resized_hat, mask):
  hat = cv2.bitwise_and(resized_hat, resized_hat, mask=mask)
  cv2.imwrite(os.path.join(__GetOutput(), 'hat.jpg'), hat)
  hat = cv2.resize(hat, (img.shape[1], img.shape[0]))
  return cv2.add(img, hat)


def AddHat(face_img, hat_img):
  r, g, b, a = cv2.split(hat_img)
  rgb_hat = cv2.merge((r, g, b))
  cv2.imwrite(os.path.join(__GetOutput(), 'hat_alpha.jpg'), a)

  # http://dlib.net/files/
  predictor_path = os.path.join(__GetOutput(), 'shape_predictor_5_face_landmarks.dat')
  predictor = dlib.shape_predictor(predictor_path)

  detector = dlib.get_frontal_face_detector()
  for d in detector(face_img, 1):
    x, y, w, h = d.left(), d.top(), d.right() - d.left(), d.bottom() - d.top()
    eye_center = __GetEyeCenter(face_img, d, predictor)

    # resize the hat according to face size
    resized_hat, resize = __ResizeImage(rgb_hat, w * 1.5, y)

    # use alpha as a mask
    mask, _ = __ResizeImage(a, w * 1.5, y)
    mask_inverse = cv2.bitwise_not(mask)

    # now calculate the hat position
    bg_roi = __GetHatArea(face_img, y, eye_center, resize)
    bg = __RemoveHatArea(bg_roi, mask_inverse)
    add_hat = __AddHat(bg, resized_hat, mask)

    # put the hat back
    face_img[y - resize[1]:y,
    (eye_center[0] - resize[0] // 3):(eye_center[0] + resize[0] // 3 * 2)] = add_hat

  return face_img


def run():
  hat_img = cv2.imread(os.path.join(__GetOutput(), 'hat.png'), -1)
  # p = re.compile('photo_wall_[0-9]+.jpg')
  # for file in os.listdir('data'):
  #   if not p.match(file):
  #     continue
  for num in [0, 178, 177, 112, 104, 139]:
    file = 'photo_wall_' + str(num) + '.jpg'
    print('processing ', file)
    face_img = cv2.imread(os.path.join(__GetOutput(), file))
    add_hat = AddHat(face_img, hat_img)
    cv2.imwrite(os.path.join(__GetOutput(), 'hat_' + file), add_hat)


if __name__ == '__main__':
  run()
