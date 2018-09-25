import pygame

from game_airplane.constants import ANIMATION_RATE


class Enemy(pygame.sprite.Sprite):

  def __init__(self, init_pos, speed=2):
    pygame.sprite.Sprite.__init__(self)

    plane_img = pygame.image.load('resources/image/shoot.png')
    self.image = plane_img.subsurface(pygame.Rect(534, 612, 57, 43))  # used to draw enemy groups

    self.down_imgs = []
    self.down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
    self.down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
    self.down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
    self.down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

    self.rect = self.image.get_rect()
    self.rect.topleft = init_pos
    self.speed = speed
    self.tick = 0
    self.hit_tick = 0

  # return should we keep running or not
  def down_draw(self, screen):
    self.tick += 1
    self.tick %= len(self.down_imgs) * ANIMATION_RATE
    screen.blit(self.down_imgs[self.tick // ANIMATION_RATE], self.rect)
    self.hit_tick += 1
    if self.hit_tick == len(self.down_imgs) * ANIMATION_RATE:
      return False
    return True

  def move(self):
    self.rect.top += self.speed
