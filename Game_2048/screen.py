class Screen(object):
  help_string1 = '(W)up (S)down (A)left (D)right'
  help_string2 = '     (R)Restart (Q)Exit'
  over_string  = '         GAME OVER!'
  win_string   = '          YOU WIN!'

  def __init__(self, screen=None, grid=None):
    self.screen = screen
    self.grid = grid

  def cast(self, string):
    self.screen.addstr(string + '\n')

  def draw_separator(self):
    self.cast('+-----' * self.grid.size + '+')

  def draw_row(self, row):
    self.cast(''.join('|{: ^5}'.format(num) if num > 0 else '|     ' for num in row) + '|')

  def draw(self, over=False, win=False):
    self.screen.clear()
    for row in self.grid.cells:
      self.draw_separator()
      self.draw_row(row)
    self.draw_separator()

    if win:
      self.cast(self.win_string)
    elif over:
      self.cast(self.over_string)
    else:
      self.cast(self.help_string1)

    self.cast(self.help_string2)