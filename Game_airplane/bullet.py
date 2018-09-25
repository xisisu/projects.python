import pygame


class Bullet(pygame.sprite.Sprite):

  def __init__(self, bullet_img, init_pos, speed=10):
    pygame.sprite.Sprite.__init__(self)
    self.image = bullet_img
    self.rect = self.image.get_rect()
    self.rect.midbottom = init_pos
    self.speed = speed

  def move(self):
    self.rect.top -= self.speed
