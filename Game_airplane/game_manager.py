import random
import pygame

from game_airplane.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SHOOT_FREQUENCY, ENEMY_FREQUENCY
from game_airplane.enemy import Enemy
from game_airplane.player import Player


class GameManager(object):
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.background = pygame.image.load('resources/image/background.png').convert()
    self.player = Player(init_pos=[200, 600], speed=8)
    self.enemies = pygame.sprite.Group()
    self.enemies_down = pygame.sprite.Group()
    self.score = 0
    self.clock = pygame.time.Clock()
    self.tick = 0

  def __shoot_bullet_and_generate_enemy(self):
    if self.tick % SHOOT_FREQUENCY == 0 and not self.player.is_hit:
      self.player.shoot()
    if self.tick % ENEMY_FREQUENCY == 0:
      self.enemies.add(
        Enemy(init_pos=[random.randint(0, SCREEN_WIDTH - pygame.Rect(534, 612, 57, 43).width), 0], speed=2))

  def __move_bullet_check_hit_enemy(self):
    for bullet in self.player.bullets:
      bullet.move()
      if bullet.rect.bottom < 0:
        self.player.bullets.remove(bullet)

    for enemy in pygame.sprite.groupcollide(self.enemies, self.player.bullets, 1, 1):
      self.enemies.remove(enemy)
      self.enemies_down.add(enemy)

  def __move_enemy_check_hit_player(self):
    for enemy in self.enemies:
      enemy.move()
      if pygame.sprite.collide_circle(enemy, self.player):
        self.enemies_down.add(enemy)
        self.enemies.remove(enemy)
        self.player.is_hit = True
        break
      if enemy.rect.top < 0:
        self.enemies.remove(enemy)

  def __draw_score(self):
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(self.score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    self.screen.blit(score_text, text_rect)

  def __handle_event(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

  def __handle_key(self):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
      self.player.move_up()
    elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
      self.player.move_down()
    elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
      self.player.move_left()
    elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
      self.player.move_right()

  def __final_score(self):
    font = pygame.font.Font(None, 48)
    text = font.render(str(self.score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = self.screen.get_rect().centerx
    text_rect.centery = self.screen.get_rect().centery + 24
    game_over = pygame.image.load('resources/image/gameover.png')
    self.screen.blit(game_over, (0, 0))
    self.screen.blit(text, text_rect)

  def run(self):
    running = True
    while running:
      self.clock.tick(60)  # frame rate of 60
      self.tick += 1
      self.__shoot_bullet_and_generate_enemy()
      self.__move_bullet_check_hit_enemy()
      self.__move_enemy_check_hit_player()

      self.screen.fill(0)
      self.screen.blit(self.background, (0, 0))
      running = self.player.draw(screen=self.screen)
      self.player.bullets.draw(self.screen)
      self.enemies.draw(self.screen)
      for enemy in self.enemies_down:
        if not enemy.down_draw(self.screen):
          self.enemies_down.remove(enemy)
          self.score += 1000
      self.__draw_score()

      pygame.display.update()
      self.__handle_event()
      self.__handle_key()

    self.__final_score()
    self.__handle_event()


if __name__ == '__main__':
  gm = GameManager()
  gm.run()
