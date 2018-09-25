from itertools import chain

from action import ACTION, Action
from grid import Grid
from screen import Screen
from state import STATE


class GameManager(object):

  def __init__(self, stdscr, size=4, win_value=2048):
    self.stdscr = stdscr
    self.size = size
    self.win_value = win_value
    self.action = Action(stdscr)
    self.grid = Grid(self.size)
    self.screen = Screen(screen=stdscr, grid=self.grid)

  def is_over(self):
    return not any(self.grid.can_move(direction) for direction in self.action.valid_directions)

  def is_win(self):
    return max(chain(*self.grid.cells)) >= self.win_value

  def state_init(self):
    self.grid.reset()
    return STATE.IN_GAME

  def state_in_game(self):
    self.screen.draw(over=self.is_over(), win=self.is_win())
    action = self.action.get()

    if action == ACTION.RESTART:
      return STATE.INIT
    elif action == ACTION.EXIT:
      return STATE.EXIT
    elif self.grid.can_move(action):
      self.grid.move(action)
      self.grid.add_random_item(count=1)
      if self.is_win() or self.is_over():
        self.screen.draw(over=self.is_over(), win=self.is_win())

    return STATE.IN_GAME

  def next_state(self, state=STATE.INIT):
    if state == STATE.INIT:
      return self.state_init()
    elif state == STATE.IN_GAME:
      return self.state_in_game()
    else:
      raise Exception('Invalid state ', state)

  def start(self):
    state = STATE.INIT
    while state != STATE.EXIT:
      state = self.next_state(state)
