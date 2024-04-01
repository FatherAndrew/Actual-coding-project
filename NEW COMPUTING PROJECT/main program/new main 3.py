
import pygame as pg
import sys

from os import path
import math

from player import Player
from obstacles import Wall
from tilemap import Map
from settings import *
from enemy import Enemy


class Game:
    def __init__(self):
        # initialize pygame
        pg.init()

        # set the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        # game control
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 10)

        self.load()

    def load(self):
        game_dir = path.dirname(__file__)
        self.map = Map(path.join(game_dir, 'map.txt'))

    def new_instance(self):
        # create a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        # create sprites
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '*':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'E':
                    self.enemy = Enemy(self, col, row)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update items in game loop
        self.all_sprites.update()

    def events(self):
        Fx = self.player.rect.centerx - self.enemy.rect.centerx
        Fy = self.player.rect.centery - self.enemy.rect.centery
        distance_x = abs(Fx)
        distance_y = abs(Fy)
       
        threshold_distance_x = 90
        threshold_distance_y = 8
        player_starting_point = (self.player.rect.centerx, self.player.rect.centery)
        starting_point = (self.enemy.rect.centerx, self.enemy.rect.centery)
        view_cone_max_vec = [-45.0, -20.0]
        view_cone_min_vec = [-25.0, -45.0]


        # handle events in game loop
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.quit()
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.player.move(dx=-0.8)
        elif keys[pg.K_d]:
            self.player.move(dx=0.8)
        if keys[pg.K_s]:
            self.player.move(dy=0.8)
        elif keys[pg.K_w]:
            self.player.move(dy=-0.8)

        if keys[pg.K_j]:
            vec_to_enemy = [self.enemy.x - starting_point[0], self.enemy.y - starting_point[1]]
            length = math.sqrt(vec_to_enemy[0]**2 + vec_to_enemy[1]**2)
            vec_to_enemy_norm = [vec_to_enemy[0]/length, vec_to_enemy[1]/length]

            min_cone_norm = [vec_to_enemy_norm[0] * math.cos(math.pi/6) - vec_to_enemy_norm[1] * math.sin(math.pi/6), 
                             vec_to_enemy_norm[0] * math.sin(math.pi/6) + vec_to_enemy_norm[1] * math.cos(math.pi/6)]
            
            max_cone_norm = [vec_to_enemy_norm[0] * math.cos(-math.pi/6) - vec_to_enemy_norm[1] * math.sin(-math.pi/6), 
                             vec_to_enemy_norm[0] * math.sin(-math.pi/6) + vec_to_enemy_norm[1] * math.cos(-math.pi/6)]
            
            view_cone_min_vec = [min_cone_norm[0]*1000, min_cone_norm[1]*1000]
            view_cone_max_vec = [max_cone_norm[0]*1000, max_cone_norm[1]*1000]
            self.enemy.move(Ex=-0.8)
        elif keys[pg.K_l]:
            
            self.enemy.move(Ex=0.8)
        if keys[pg.K_k]:
            self.enemy.move(Ey=0.8)
        elif keys[pg.K_i]:
            self.enemy.move(Ey=-0.8)
        
        view_cone_max_end_point = [starting_point[0] + view_cone_max_vec[0], starting_point[1] + view_cone_max_vec[1]]
        view_cone_min_end_point = [starting_point[0] + view_cone_min_vec[0], starting_point[1] + view_cone_min_vec[1]]
        pg.draw.line(self.screen, pg.Color("#0000ff"), starting_point, view_cone_max_end_point)
        pg.draw.line(self.screen, pg.Color("#0000ff"), starting_point, view_cone_min_end_point)

        if self.player.check_if_player_is_in_cone(starting_point, view_cone_min_vec, view_cone_max_vec, player_starting_point):
            print("success")
        else:
            print("no work")
        
        """if distance_x > threshold_distance_x:
            if self.player.x < self.enemy.x:
                self.enemy.move(Ex=-0.4)
            elif self.player.x > self.enemy.x:
                self.enemy.move(Ex=0.4)
        elif distance_y > threshold_distance_y:
            if self.player.y > self.enemy.y:
                self.enemy.move(Ey=0.4)
            elif self.player.y < self.enemy.y:
                self.enemy.move(Ey=-0.4)"""
         

    def draw(self):
        # draw items in game loop
        self.player.point_at(*pg.mouse.get_pos())
        #self.enemy.point_at_player(self.player.rect.centerx,self.player.rect.centery)
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)


        # flip display after drawing
        pg.display.flip()


if __name__ == "__main__":
    g = Game()

    while True:
        g.new_instance()
        g.run()
