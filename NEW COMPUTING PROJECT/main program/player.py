import pygame as pg
import math
from Bullet import Bullet
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pg.math.Vector2(13, 20)
        self.original_image = pg.image.load('playersprite.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.velocity = 0.25
        self.last_shot = 0
        self.cooldown = 750
        self.shoot = False
        self.direction = 0
        self.player_health = 35
        self.x = x
        self.y = y
        self.hitbox = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)


    def colliding_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == round(self.x + dx * self.velocity) and wall.y == round(self.y + dy * self.velocity):
                return True
        return False
    
    def point_at(self, x, y):
        direction_new = pg.math.Vector2(x, y) - self.rect.center
        angle = direction_new.angle_to((0, -1))
        self.image = pg.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        dx = x - self.rect.centerx
        dy = y - self.rect.centery
        self.direction = math.degrees(math.atan2(-dy, dx))

    def bullet_thing(self):
        current_time = pg.time.get_ticks()  
        
        if current_time - self.last_shot > self.cooldown:
            bullet = Bullet(self.game, self.rect.centerx, self.rect.centery, self.direction, owner='player')
            self.game.all_sprites.add(bullet)
            self.game.player_bullets.add(bullet)
            self.last_shot = current_time
    
    def update_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery


    def move(self, dx=0, dy=0):
        
        if not self.colliding_with_walls(dx, dy):
            self.x += dx * self.velocity
            self.y += dy * self.velocity
            self.rect.x = self.x * 32
            self.rect.y = self.y *32
            self.update_hitbox()

    def update(self):
        self.rect.x = self.x* 32
        self.rect.y = self.y*32
        self.update_hitbox()