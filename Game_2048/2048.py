import curses

from game_manager import GameManager


def main(stdsrc):
  game_manager = GameManager(stdscr=stdsrc, size=4, win_value=32)
  game_manager.start()


if __name__ == '__main__':
  curses.wrapper(main)
