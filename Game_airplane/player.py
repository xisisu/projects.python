import pygame

from bullet import Bullet

from game_airplane.constants import SCREEN_HEIGHT, SCREEN_WIDTH, ANIMATION_RATE


class Player(pygame.sprite.Sprite):

  def __init__(self, init_pos, speed=8):
    pygame.sprite.Sprite.__init__(self)

    plane_img = pygame.image.load('resources/image/shoot.png')

    self.normal_imgs = []
    self.normal_imgs.append(plane_img.subsurface(pygame.Rect(0, 99, 102, 126)))
    self.normal_imgs.append(plane_img.subsurface(pygame.Rect(165, 360, 102, 126)))

    self.down_imgs = []
    self.down_imgs.append(plane_img.subsurface(pygame.Rect(165, 234, 102, 126)))
    self.down_imgs.append(plane_img.subsurface(pygame.Rect(330, 624, 102, 126)))
    self.down_imgs.append(plane_img.subsurface(pygame.Rect(330, 498, 102, 126)))
    self.down_imgs.append(plane_img.subsurface(pygame.Rect(432, 624, 102, 126)))

    self.rect = self.normal_imgs[0].get_rect()
    self.rect.topleft = init_pos
    self.speed = speed
    self.bullets = pygame.sprite.Group()
    self.tick = 0
    self.hit_tick = 0
    self.is_hit = False

  # return should we keep running or not
  def draw(self, screen):
    self.tick += 1
    if self.is_hit:
      self.tick %= len(self.down_imgs) * ANIMATION_RATE
      screen.blit(self.down_imgs[self.tick // ANIMATION_RATE], self.rect)
      self.hit_tick += 1
      if self.hit_tick == len(self.down_imgs) * ANIMATION_RATE:
        return False
    else:
      self.tick %= len(self.normal_imgs) * ANIMATION_RATE
      screen.blit(self.normal_imgs[self.tick // ANIMATION_RATE], self.rect)
    return True

  def shoot(self):
    plane_img = pygame.image.load('resources/image/shoot.png')
    bullet = Bullet(bullet_img=plane_img.subsurface([1004, 987, 9, 21]), init_pos=self.rect.midtop, speed=10)
    self.bullets.add(bullet)

  def move_up(self):
    self.rect.top -= self.speed
    if self.rect.top <= 0:
      self.rect.top = 0

  def move_down(self):
    self.rect.top += self.speed
    if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
      self.rect.top = SCREEN_HEIGHT - self.rect.height

  def move_left(self):
    self.rect.left -= self.speed
    if self.rect.left <= 0:
      self.rect.left = 0

  def move_right(self):
    self.rect.left += self.speed
    if self.rect.left >= SCREEN_WIDTH - self.rect.width:
      self.rect.left = SCREEN_WIDTH - self.rect.width
