# import
import pygame
import random
import time
import numpy as np
import re
import math

# define things
WIDTH = 720
HEIGHT = 480
SCREEN_SIZE = (WIDTH, HEIGHT)
BG_COLOR = (20, 20, 20)

# initialize
pygame.display.init()

# pygame.mixer.pre_init(44100, -16, 1, 512)
# pygame.mixer.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

# WALL_HIT_SOUND = pygame.mixer.Sound('audio/basic_fist_hit.wav')

# ICON = pygame.image.load('enemy_100px.png')
# pygame.display.set_icon(ICON)
# pygame.display.set_caption("StopCovid19")

# WALL_HIT_SOUND.play()


# exit()
# time.sleep(100)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, img='img/enemy_48.png', speed_x=2, speed_y=2, x=0, y=0, groups=[]):
        super().__init__(*groups)
        self.screen = screen
        # self.img = pygame.image.load(img)
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.img)
        # self.mass = 4/3 * np.pi * (int(re.search(r'(\d{1,3})\.png',img).group(1)) // 2 )**3
        self.radius = int(re.search(r'(\d{1,3})\.png',img).group(1)) // 2 
        self.mass = self.radius**3

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.update_x_width = self.rect.width + abs(self.speed_x)
        self.update_y_width = self.rect.height + abs(self.speed_y)


    def get_mass(self):
        return self.mass

    def set_center(self, x, y):
        self.rect.center = (x, y)

    def get_center_x(self):
        return self.rect.center[0]

    def get_center_y(self):
        return self.rect.center[1]

    def get_speed_x(self):
        return self.speed_x

    def get_speed_y(self):
        return self.speed_y


    def set_speed(self, x_num, y_num):
        self.speed_x = x_num
        self.speed_y = y_num

        # update rectangles for updates
        self.update_x_width = self.rect.width + abs(self.speed_x)
        self.update_y_width = self.rect.height + abs(self.speed_y)


    def increase_speed_by(self, delta_x, delta_y):
        x, y = self.get_speed_x(), self.get_speed_y()
        self.set_speed(x + delta_x, y + delta_y)


    def draw(self):
        self.screen.blit(self.img, self.rect)


    def reverse_x_speed(self):
        self.speed_x *= -1

    def reverse_y_speed(self):
        self.speed_y *= -1


    def move(self):
        '''move to current direction'''
        global WIDTH, HEIGHT

        # print('\nStarting Position: ', list(self.rect))
        new_x = self.rect.x + self.speed_x
        new_y = self.rect.y + self.speed_y

        update_region = [
                        [new_x, self.rect.x][self.speed_x > 0] ,
                        [new_y, self.rect.y][self.speed_y > 0] ,
                        self.update_x_width,
                        self.update_y_width
                        ]

        # screen borders
        if not 0 <= new_x <= (WIDTH - self.rect.width):
            new_x = min(new_x, WIDTH - self.rect.width)
            new_x = max(new_x, 0)
            self.reverse_x_speed()

        if not 0 <= new_y <= (HEIGHT - self.rect.height):
            new_y = min(new_y, HEIGHT - self.rect.height)
            new_y = max(new_y, 0)
            self.reverse_y_speed()

        self.rect.x = new_x
        self.rect.y = new_y

        self.draw()
        
        return update_region


    def collide(self, other):
        '''
        update speeds if collision happens
        '''
        dx = self.get_center_x() - other.get_center_x()
        dy = self.get_center_y() - other.get_center_y()

        distance = math.hypot(dx, dy)


        if distance < self.radius + other.radius:
            tangent = math.atan2(dy, dx)
            # not sure
            angle_1 = np.arctan2(self.get_center_y(), self.get_center_x())
            angle_2 = np.arctan2(other.get_center_y(), other.get_center_x())
            ####
            speed_1 = (self.get_speed_x(), self.get_speed_y())
            speed_2 = (other.get_speed_x(), other.get_speed_y())
            self.set_speed(*speed_2)
            other.set_speed(*speed_1)

            # correction
            angle = 0.5 * math.pi + tangent
            self.set_center(self.get_center_x() + math.sin(angle), self.get_center_y() - math.cos(angle))
            other.set_center(other.get_center_x() - math.sin(angle), other.get_center_y() + math.cos(angle))
            # print('Boom')



# def main():        
enemies_num = 8
enemy_pics = [
                # 'img/enemy_16.png',
                # 'img/enemy_32.png',
                'img/enemy_48.png',
                # 'img/enemy_64.png',
                # 'img/enemy_84.png',
                # 'img/enemy_84.png',
                # 'img/enemy_84.png',
            ] * enemies_num


ALL_SPRITES = pygame.sprite.Group()

enemies = [
            Enemy(
                screen=screen,
                # x=random.choice(range((WIDTH // enemies_num) *i, (WIDTH // enemies_num)  * (i+1))),
                # y=random.choice(range((HEIGHT // enemies_num) *i, (HEIGHT // enemies_num)  * (i+1))),
                x=random.choice(range(WIDTH)),
                y=random.choice(range(HEIGHT)),
                speed_x=random.randint(1, 10),
                speed_y=random.randint(1, 10),
                img=enemy_pics[i],
                groups=ALL_SPRITES,
                )

            for i in range(enemies_num)]

ALL_SPRITES.add(enemies)

# GO
screen.fill(BG_COLOR)
pygame.display.update()


FPS = 30

run = 1
while run:
    pygame.time.wait(1000 // FPS)
    # time.sleep(1000 // FPS / 1000)

    # EXIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = 0

    # UPDATE
    screen.fill(BG_COLOR)

    for index, enemy in enumerate(enemies):
        enemy.move()
        for enemy_2 in enemies[index + 1:]:
            enemy.collide(enemy_2)
    pygame.display.update()

    # redraw player

pygame.quit()


# if __name__ == '__main__':
#     main()
# 
