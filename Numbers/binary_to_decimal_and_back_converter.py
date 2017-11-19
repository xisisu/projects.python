"""
Binary to Decimal and Back Converter - Develop a converter to convert a decimal number to binary or a binary number
to its decimal equivalent.
"""


def ConvertBinaryToDecimal(n):
  return int(n, 2)


def ConvertDecimalToBinary(n):
  return bin(n)[2:]


def run():
  while True:
    n = input('Enter the number in binary: ')
    if n in ('quit', 'exit'):
      return
    elif not n.isdigit():
      print('{} is not a digit'.format(n))
    elif int(n) <= 0:
      print('{} must be greater than 0.'.format(n))
    else:
      decimal = ConvertBinaryToDecimal(n)
      binary = ConvertDecimalToBinary(decimal)
      print('{} to {} to {}'.format(n, decimal, binary))


if __name__ == '__main__':
  run()
