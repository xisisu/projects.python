# https://gist.github.com/haojian/0ee6dd444994fd67f63b

import cv2
import numpy as np
from skimage import data
from skimage.color import label2rgb
from skimage.filters import threshold_otsu
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.segmentation import clear_border


def run(filename):
  img = data.imread(filename, as_grey=True)
  threshold = threshold_otsu(img)
  bw = closing(img > threshold, square(1))
  cleared = bw.copy()
  clear_border(cleared)

  label_image = label(cleared)
  borders = np.logical_xor(bw, cleared)
  label_image[borders] = -1
  colors = np.random.rand(300, 3)
  background = np.random.rand(3)
  image_label_overlay = label2rgb(label_image, image=img, colors=colors, bg_color=background)
  cv2.imwrite('Done.jpg', image_label_overlay * 255)


if __name__ == '__main__':
  run('images/img1.jpg')
