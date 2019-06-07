import random

class TicTacToe:
  EMPTY = ' '
  PLAYER = 'P'
  AI = 'A'
  
  def __init__(self, board_size=3):
    self.board_size = board_size
    self.board = [self.EMPTY] * (self.board_size ** 2)

  def display_board(self):
    print('Board:')
    for i in range(self.board_size):
      row = self.board[i*self.board_size: (i+1)*self.board_size]
      print ('|'.join(row))
  
  def display_movement(self):
    print('Movement key:')
    for i in range(self.board_size):
      row = range((i)*self.board_size+1, (i+1)*self.board_size+1)
      print ('|'.join(map(str, row)))

  def get_player_pos(self):
    while True:
      try:
        pos = int(raw_input('where to? '))
      except ValueError:
        print ('invalid movement key')
        continue      
      if pos <= 0 or pos > self.board_size**2:
        print ('pos out of range')
        continue
      if self.board[pos-1] != self.EMPTY:
        print ('pos taken')
        continue
      return pos-1 # get the real index.
  
  def place_cell(self, pos, value):
    if self.board[pos] != self.EMPTY:
      print('taken')
      return    
    self.board[pos] = value
    self.display_board()

  def get_ai_pos(self):
    gain = map(lambda x : x**2, self.compute_score_for_all_cells(self.AI))
    risk = map(lambda x : x**2, self.compute_score_for_all_cells(self.PLAYER))    
    scores = [gain[idx] + risk[idx] for idx in range(len(gain))]
    max_score = max(scores)
    if max_score == 0: # all cells are taken.
      return None
    return random.choice([idx for idx in range(len(scores)) if scores[idx] == max_score])

  def is_game_over(self, pos):
    return self.get_max_score_at_one_cell(pos, self.board[pos]) >= self.board_size

  def compute_score_for_all_cells(self, value):
    assert value != self.EMPTY
    return [0 if self.board[pos] != self.EMPTY else self.get_max_score_at_one_cell(pos, value) for pos in range(len(self.board))]

  def get_max_score_at_one_cell(self, pos, value):
    assert value != self.EMPTY
    u_d = sum(self.check_same_value_one_direction(pos, dx, dy, value) for (dx, dy) in [(1, 0), (-1, 0)]) + 1
    l_r = sum(self.check_same_value_one_direction(pos, dx, dy, value) for (dx, dy) in [(0, 1), (0, -1)]) + 1
    ul_dr = sum(self.check_same_value_one_direction(pos, dx, dy, value) for (dx, dy) in [(-1, -1), (1, 1)]) + 1
    ur_dl = sum(self.check_same_value_one_direction(pos, dx, dy, value) for (dx, dy) in [(1, -1), (-1, 1)]) + 1
    return max(u_d, l_r, ul_dr, ur_dl)

  def check_same_value_one_direction(self, pos, dx, dy, value):    
    x, y = pos // self.board_size + dx, pos % self.board_size + dy
    count = 0
    while 0 <= x < self.board_size and 0 <= y < self.board_size:
      if self.board[x*self.board_size+y] != value:
        return count
      count += 1
      x, y = x + dx, y + dy
    return count
  
if __name__ == '__main__':
  board = TicTacToe(board_size=3)
  board.display_movement()
  board.display_board()
  while True:
    player = board.get_player_pos()
    board.place_cell(player, TicTacToe.PLAYER)
    if board.is_game_over(player):
      print('player win!')
      break
    ai = board.get_ai_pos()
    if ai is None: # no more moves
      print('draw!')
      break
    board.place_cell(ai, TicTacToe.AI)
    if board.is_game_over(ai):
      print('ai win!')
      break