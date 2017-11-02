"""
Find Cost of Tile to Cover W x H Floor - Calculate the total cost of tile it would take to cover a floor plan of width
and height, using a cost entered by the user.
"""


def run():
  weight = input('Enter width: ')
  height = input('Enter height: ')
  cost_per_tile = input('Enter cost per tile: ')
  print('cost is {}'.format(float(weight) * float(height) * float(cost_per_tile)))


if __name__ == '__main__':
  run()
