from enum import Enum, unique, auto


@unique
class ACTION(Enum):
  UP = auto()
  DOWN = auto()
  LEFT = auto()
  RIGHT = auto()
  RESTART = auto()
  EXIT = auto()

class Action(object):
  # constants
  valid_char = [ord(ch) for ch in 'WASDRQwasdrq']
  valid_action = [ACTION.UP, ACTION.LEFT, ACTION.DOWN, ACTION.RIGHT, ACTION.RESTART, ACTION.EXIT]
  action_dict = dict(zip(valid_char, valid_action * 2))
  valid_directions = [ACTION.UP, ACTION.LEFT, ACTION.DOWN, ACTION.RIGHT]

  def __init__(self, stdscr):
    self.stdscr = stdscr

  def get(self):
    char = self.stdscr.getch()
    while char not in self.valid_char:
      char = self.stdscr.getch()
    return self.action_dict[char]