import pygame as pg
import sys

from os import path
import math

from player import Player
from obstacles import Wall
from tilemap import Map
from settings import *
from enemy import Enemy
from Bullet import Bullet
from pygame.locals import *
screen = pg.display.set_mode((WIDTH, HEIGHT))

pg.init()

# Set up the display
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)

# Define colors
WHITE = (255, 255, 255)

# Define button parameters
mainClock = pg.time.Clock()
x = 100
y = 200
w = 200
h = 50
font = pg.font.Font(None, 20)

def start_game():
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

            self.view_cone_min_vec = [10, 15]
            self.view_cone_max_vec = [-15, 15]

            self.check_x = 0
            self.check_y = 0

            self.all_sprites = pg.sprite.Group()
            self.walls = pg.sprite.Group()
            self.bullets = pg.sprite.Group()
            self.enemies = pg.sprite.Group()
            self.player_bullets = pg.sprite.Group()  
            self.enemy_bullets = pg.sprite.Group()   
            self.load()

        def load(self):
            game_dir = path.dirname(__file__)
            self.map = Map(path.join(game_dir, 'map.txt'))

        def new_instance(self):
            # create a new game
            self.all_sprites = pg.sprite.Group()
            self.walls = pg.sprite.Group()
            self.enemies = pg.sprite.Group()
            # Create sprites
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == '*':
                        Wall(self, col, row)
                    elif tile == 'P':
                        self.player = Player(self, col, row)
                    elif tile == 'E':
                        self.enemy = Enemy(self, col, row)
                        self.check_x, self.check_y = col, row
                        self.enemies.add(self.enemy)
        

        def run(self):
            # game loop
            self.playing = True
            while self.playing:
                self.dt = self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()
                pg.display.flip()

        def quit(self):
            pg.quit()
            sys.exit()

        def update(self):
            self.all_sprites.update()
            self.player_bullets.update()
            self.enemy_bullets.update()

            # Check for collisions between player bullets and enemies
            for bullet in self.player_bullets:
                if pg.sprite.spritecollideany(bullet, self.enemies):
                    bullet.kill()
                    self.enemy.enemy_health -= 5

            # Check for collisions between enemy bullets and player
            for bullet in self.enemy_bullets:
                if pg.sprite.spritecollideany(bullet, [self.player]) and self.enemy.enemy_health > 0:
                    bullet.kill()
                    self.player.player_health -= 5




        def check_if_player_is_in_cone(self, starting_point, cone_min_vec, cone_max_vec, player_pos):
            # Calculate vector from starting point to player
            vec_to_player = [player_pos[0] - starting_point[0], player_pos[1] - starting_point[1]]

            # Calculate angles between vectors
            angle_min = math.atan2(cone_min_vec[1], cone_min_vec[0])
            angle_max = math.atan2(cone_max_vec[1], cone_max_vec[0])
            angle_player = math.atan2(vec_to_player[1], vec_to_player[0])

            # Calculate distance between starting point and player
            distance = math.sqrt((vec_to_player[0] ** 2) + (vec_to_player[1] ** 2))

            # Check if the player is within the angle and distance range
            if angle_min <= angle_player <= angle_max and distance <= MAX_VISION_DISTANCE:
                return True
            else:
                return False

        def events(self):
            # handle events in game loop
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.quit()

            vec_to_enemy = [self.player.rect.centerx - self.enemy.rect.centerx,
                            self.player.rect.centery - self.enemy.rect.centery]
            length = math.sqrt(vec_to_enemy[0]**2 + vec_to_enemy[1]**2)

            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                self.player.move(dx=-0.8)
            elif keys[pg.K_d]:
                self.player.move(dx=0.8)
            if keys[pg.K_s]:
                self.player.move(dy=0.8)

            elif keys[pg.K_w]:
                self.player.move(dy=-0.8)
            if keys[pg.K_SPACE] or pg.mouse.get_pressed() == (1,0,0):
                self.player.shoot = True
                self.player.bullet_thing()
            else:
                self.player.shoot = False

            if keys[pg.K_g] or pg.mouse.get_pressed() == (0,0,1):
                self.enemy.shoot = True
                self.enemy.bullet_thing()
            else:
                self.player.shoot = False

            if self.check_if_player_is_in_cone(self.enemy.rect.center, self.view_cone_min_vec, self.view_cone_max_vec,
                                            (self.player.rect.centerx, self.player.rect.centery)) and self.enemy.enemy_health > 0:

                #enemy move towards player if in the LOS
                self.enemy.point_at_player(self.player.rect.centerx, self.player.rect.centery)
                self.enemy.shoot = True
                self.enemy.bullet_thing()
                if length > 120:
                    self.enemy.move(vec_to_enemy[0] * 0.4 / length, vec_to_enemy[1] * 0.4 / length)
            else:
                self.enemy.return_to_original_pos(self.check_x, self.check_y)
                

        def draw(self):
            starting_point = (self.enemy.rect.centerx, self.enemy.rect.centery)
            vision_distance = 10  

            view_cone_min_end_point = [starting_point[0] + self.view_cone_min_vec[0] * vision_distance,
                                    starting_point[1] + self.view_cone_min_vec[1] * vision_distance]
            view_cone_max_end_point = [starting_point[0] + self.view_cone_max_vec[0] * vision_distance,
                                    starting_point[1] + self.view_cone_max_vec[1] * vision_distance]
            
            self.player.point_at(*pg.mouse.get_pos())
            self.screen.fill(WHITE)
            
            if self.enemy.enemy_health <= 0:
                self.enemy.shoot = False
                self.all_sprites.remove(self.enemy)
                self.all_sprites.draw(self.screen)
            elif self.player.player_health <= 0:
                exit()
            else:
                self.all_sprites.draw(self.screen) 
                #pg.draw.rect(self.screen, pg.Color('blue'), self.enemy.hitbox, 2)
                pg.draw.line(self.screen, pg.Color("blue"), starting_point, view_cone_min_end_point, 2)
                pg.draw.line(self.screen, pg.Color("blue"), starting_point, view_cone_max_end_point, 2) 

                pg.draw.rect(self.screen, pg.Color('green'), (self.enemy.rect.x, self.enemy.rect.y - 10, self.enemy.enemy_health, 5))
            pg.draw.rect(self.screen, pg.Color('green'), (self.player.rect.x, self.player.rect.y - 10, self.player.player_health, 5))
            self.player_bullets.draw(self.screen)  
            self.enemy_bullets.draw(self.screen)   
            #pg.draw.rect(self.screen, pg.Color('red'), self.player.hitbox, 2)
            
            pg.display.flip()


    if __name__ == "__main__":
        g = Game()

        while True:
            g.new_instance()
            g.run()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill((73, 77, 95))

        mx, my = pg.mouse.get_pos()

        button_1 = pg.Rect(WIDTH / 2 - 100, 100, 200, 50)
        button_2 = pg.Rect(WIDTH / 2 - 100, 200, 200, 50)
        
        pg.draw.rect(screen, (132, 88, 179), button_1)
        pg.draw.rect(screen, (132, 88, 179), button_2)
        draw_text('Start Game', font, WHITE, screen, WIDTH / 2.1, 120)
        draw_text('Options', font, WHITE, screen, WIDTH / 2.1, 220)

        # Check for button clicks
        if button_1.collidepoint((mx, my)):
            if click:
                start_game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pg.display.update()
        mainClock.tick(60)

def options():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text('Options', font, WHITE, screen, WIDTH / 2, HEIGHT / 2)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pg.display.update()
        mainClock.tick(60)

main_menu()