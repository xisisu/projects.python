# https://www.shiyanlou.com/courses/370/labs/1191/document

from PIL import Image
import argparse

def init_args():
  parser = argparse.ArgumentParser()

  parser.add_argument('-i', '--input')
  parser.add_argument('-w', '--width', type=int, default=60)
  parser.add_argument('--height', type=int, default=60)
  parser.add_argument('-o', '--output')

  args = parser.parse_args()
  return args.input, args.width, args.height, args.output

ASCII_CHAR = list(" $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.")

# based on rgb, select a constant char.
def get_char(r, g, b, alpha=256):
  # range is 0 to 255
  gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
  return ASCII_CHAR[int((gray / 256.0) * len(ASCII_CHAR))]

def run():
  input, width, height, output = init_args()
  image = Image.open(input)
  image = image.resize((width, height), Image.NEAREST)

  txt = ""
  for i in range(height):
    for j in range(width):
      txt += get_char(*image.getpixel((j, i)))
    txt += '\n'
  print(txt)

  if output:
    with open(output, 'w') as f:
      f.write(txt)

if __name__ == '__main__':
  run()
