import random

from action import ACTION


class Grid(object):

  def __init__(self, size):
    self.size = size
    self.cells = None
    self.reset()

  def reset(self):
    self.cells = [[0 for _ in range(self.size)] for _ in range(self.size)]
    self.add_random_item(count=2)

  def add_random_item(self, count=1):
    empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.cells[i][j] == 0]
    for _ in range(count):
      (i, j) = random.choice(empty_cells)
      empty_cells.remove((i, j))
      self.cells[i][j] = 4 if random.randrange(100) >= 90 else 2

  def transpose(self):
    self.cells = [list(row) for row in zip(*self.cells)]

  def invert(self):
    self.cells = [row[::-1] for row in self.cells]

  # For testing only.
  def fill_for_test(self):
    self.cells = [[2 if random.randrange(100) <= 50 else 4 for _ in range(self.size)] for _ in range(self.size)]

  @staticmethod
  def move_row_left(row):
    # move all elements to left, fill rest with 0s
    def tighten(row):
      new_row = [i for i in row if i != 0]
      new_row += [0 for i in range(len(row) - len(new_row))]
      return new_row

    def merge(row):
      new_row = row
      for i in range(len(new_row)):
        if i + 1 < len(row) and new_row[i] == new_row[i + 1]:
          new_row[i] = 2 * new_row[i]
          new_row[i + 1] = 0
          i += 1
      return new_row

    return tighten(merge(tighten(row)))

  def move_left(self):
    self.cells = [self.move_row_left(row) for row in self.cells]

  def move_right(self):
    self.invert()
    self.move_left()
    self.invert()

  def move_up(self):
    self.transpose()
    self.move_left()
    self.transpose()

  def move_down(self):
    self.transpose()
    self.move_right()
    self.transpose()

  def move(self, direction=None):
    if direction == ACTION.UP:
      self.move_up()
    elif direction == ACTION.DOWN:
      self.move_down()
    elif direction == ACTION.LEFT:
      self.move_left()
    elif direction == ACTION.RIGHT:
      self.move_right()
    else:
      raise Exception('Invalid direction ', direction)

  @staticmethod
  def can_move_row_left(row):
    return row != Grid.move_row_left(row)

  # TODO: figure out a way to optimize the redundant code below.
  def can_move_left(self):
    return any(self.can_move_row_left(row) for row in self.cells)

  def can_move_right(self):
    self.invert()
    can = self.can_move_left()
    self.invert()
    return can

  def can_move_up(self):
    self.transpose()
    can = self.can_move_left()
    self.transpose()
    return can

  def can_move_down(self):
    self.transpose()
    can = self.can_move_right()
    self.transpose()
    return can

  def can_move(self, direction=None):
    if direction == ACTION.UP:
      return self.can_move_up()
    elif direction == ACTION.DOWN:
      return self.can_move_down()
    elif direction == ACTION.LEFT:
      return self.can_move_left()
    elif direction == ACTION.RIGHT:
      return self.can_move_right()
    else:
      raise Exception('Invalid direction ', direction)
