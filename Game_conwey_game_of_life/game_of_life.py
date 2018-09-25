# http://web.stanford.edu/~cdebs/GameOfLife/

import curses
import random

from itertools import product
from time import sleep


class GameOfLife(object):

  def __init__(self, stdscr, width, height):
    self.stdscr = stdscr
    self.size = (width, height)
    # self.random_world()
    self.organize_world()
    print(type(self.live_cells))
    print(self.live_cells)

  def random_world(self):
    width, height = self.size
    world = product(range(width), range(height))
    self.live_cells = {cell for cell in world if random.randrange(100) >= 90}

  def evolve(self):
    width, height = self.size
    world = product(range(width), range(height))
    self.live_cells = {cell for cell in world if self.evolve_cell(cell=cell)}

  def evolve_cell(self, cell):
    alive = cell in self.live_cells
    neighbours = self.count_neighbours(cell=cell)
    return neighbours == 3 or (alive and neighbours == 2)

  def count_neighbours(self, cell):
    x, y = cell
    deltas = set(product([-1, 0, 1], repeat=2)) - set([(0, 0)])
    neighbours = ((x + dx, y + dy) for (dx, dy) in deltas)
    return sum(neighbor in self.live_cells for neighbor in neighbours)

  def draw(self):
    self.stdscr.clear()
    width, height = self.size
    for x in range(width):
      string = ''.join(self.draw_cell(x, y) for y in range(height))
      self.stdscr.addstr(string + '\n')
    self.stdscr.refresh()

  def draw_cell(self, x, y):
    cell = (x, y)
    return '0' if cell in self.live_cells else ' '

  def organize_world(self):
    width, height = self.size
    if width <= 40 or height <= 40:
      print('Cannot init with a small graph.')
      exit()

    self.live_cells = set()

    ############## static blocks #############
    # block
    self.live_cells = self.live_cells.union(set([(1, 1), (1, 2), (2, 1), (2, 2)]))

    # boat
    self.live_cells = self.live_cells.union(set([(1, 5), (1, 6), (2, 5), (2, 7), (3, 6)]))

    # loaf
    self.live_cells = self.live_cells.union(set([(1, 10), (1, 11), (2, 9), (2, 12), (3, 10), (3, 12), (4, 11)]))

    # beehive
    self.live_cells = self.live_cells.union(set([(1, 16), (1, 17), (2, 15), (2, 18), (3, 16), (3, 17)]))

    ########### blink blocks ##############
    # blinker
    self.live_cells = self.live_cells.union(set([(10, 1), (10, 2), (10, 3)]))

    # beacon
    self.live_cells = self.live_cells.union(
      set([(10, 7), (10, 8), (11, 7), (11, 8), (12, 9), (12, 10), (13, 9), (13, 10)]))

def main(stdsrc):
  game_of_life = GameOfLife(stdscr=stdsrc, width=50, height=50)
  for _ in range(10):
    game_of_life.draw()
    game_of_life.evolve()
    sleep(0.1)


if __name__ == '__main__':
  curses.wrapper(main)
