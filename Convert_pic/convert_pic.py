# https://www.shiyanlou.com/courses/589/labs/1964/document

from PIL import Image
import argparse


class Converter(object):

  def __init__(self, image):
    self.image = image if isinstance(image, Image.Image) else Image.open(image)
    self.width, self.height = self.image.size

  @staticmethod
  def is_skin_rgb(r, g, b):
    return r > 95 and \
           g > 40 and g < 100 and \
           b > 20 and \
           max([r, g, b]) - min([r, g, b]) > 15 and \
           abs(r - g) > 15 and \
           r > g and \
           r > b

  @staticmethod
  def is_skin_normalized_rgb(r, g, b):
    def normalize(r, g, b):
      r = 0.0001 if r == 0 else r
      g = 0.0001 if g == 0 else g
      b = 0.0001 if b == 0 else b
      _sum = float(r + g + b)
      return [r / _sum, g / _sum, b / _sum]

    nr, ng, nb = normalize(r, g, b)
    return nr / ng > 1.185 and \
           float(r * b) / ((r + g + b) ** 2) > 0.107 and \
           float(r * g) / ((r + g + b) ** 2) > 0.112

  @staticmethod
  def is_skin_ycbcr(r, g, b):
    def to_ycbcr(r, g, b):
      # http://stackoverflow.com/questions/19459831/rgb-to-ycbcr-conversion-problems
      y = .299 * r + .587 * g + .114 * b
      cb = 128 - 0.168736 * r - 0.331364 * g + 0.5 * b
      cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b
      return y, cb, cr

    y, cb, cr = to_ycbcr(r, g, b)
    return 97.5 <= cb <= 142.5 and \
           134 <= cr <= 176

  @staticmethod
  def is_skin(r, g, b, method='ycbcr'):
    if method == 'ycbcr':
      return Converter.is_skin_ycbcr(r, g, b)
    elif method == 'rgb':
      return Converter.is_skin_rgb(r, g, b)
    elif method == 'rgbn':
      return Converter.is_skin_normalized_rgb(r, g, b)

  def parse(self, method='ycbcr'):
    new_image = self.image
    new_data = new_image.load()

    pixels = self.image.load()
    for y in range(self.height):
      for x in range(self.width):
        r, g, b = pixels[x, y]
        if self.is_skin(r, g, b, method=method):
          new_data[x, y] = 255, 255, 255
        else:
          new_data[x, y] = 0, 0, 0

    return new_image


def run():
  parser = argparse.ArgumentParser(description='Detect nudity in images.')
  parser.add_argument('-i', '--input')
  parser.add_argument('-o', '--output')
  parser.add_argument('-m', '--method', type=str, default='ycbcr')
  args = parser.parse_args()

  nude = Converter(args.input)
  new_image = nude.parse(args.method)
  new_image.save(args.output)


if __name__ == '__main__':
  run()
