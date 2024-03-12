import  pygame
from settings import *
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction, owner):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.originial_image = pygame.image.load("NewBullet_img.png").convert_alpha()
        self.image = self.originial_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.speed = 5
        self.damage = 5
        self.direction = direction
        self.bullet_lifetime = 750
        self.spawn_time = pygame.time.get_ticks()
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.rect.width + 1, self.rect.height + 1)
        self.owner = owner
    
    def Update_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery
    
    def bullet_movement(self):
        self.x += self.x * self.speed
        self.y += self.y * self.speed
        self.rect.x = int(self.x)*32
        self.rect.y = int(self.y)*32
        self.Update_hitbox()

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()
    
    def update(self):
        # Move the bullet in the specified direction
        self.rect.x += self.speed * math.cos(math.radians(self.direction))
        self.rect.y -= self.speed * math.sin(math.radians(self.direction))
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery

        # Check if the bullet has reached its lifetime
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()



    



