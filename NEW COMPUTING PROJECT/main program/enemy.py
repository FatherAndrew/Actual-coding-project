import pygame
import math
from settings import *
from Bullet import *

				

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.original_image = pygame.image.load("new_enemysprite.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.start_position = (8, 5)
        self.last_shot = 0
        self.cooldown = 750
        self.shoot = False
        self.direction = 0
        self.enemy_health = 35
        self.x = x
        self.y = y
        self.movespeed = 0.25
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        

    def enemy_collide_wall(self, Ex=0, Ey=0):
        for wall in self.game.walls:
            if wall.x == round(self.x + Ex * self.movespeed) and wall.y == round(self.y + Ey * self.movespeed):
                return True
        return False


    def point_at_player(self, Ex, Ey):
        direction = pygame.math.Vector2(Ex, Ey) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        dx = Ex - self.rect.centerx
        dy = Ey - self.rect.centery
        self.direction = math.degrees(math.atan2(-dy, dx))

    def bullet_thing(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.cooldown:
            bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, self.direction, owner='enemy')
            self.game.all_sprites.add(bullet)
            self.game.enemy_bullets.add(bullet)
            self.last_shot = current_time

    def return_to_original_pos(self, x,y):
        if round(self.x) > x:
            self.x -= self.movespeed
        elif round(self.x) < x:
            self.x += self.movespeed
        if round(self.y) > y:
            self.y -= self.movespeed
        elif round(self.y) < y:
            self.y += self.movespeed

    def update_enemy_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery

    def move(self, Ex=0, Ey=0):
        if not self.enemy_collide_wall(Ex, Ey):
            self.x += Ex * self.movespeed
            self.y += Ey * self.movespeed
            self.rect.x = self.x * 32
            self.rect.y = self.y * 32
            self.update_enemy_hitbox()

    def update(self):
        self.rect.x = self.x * 32
        self.rect.y = self.y * 32
        self.update_enemy_hitbox()
