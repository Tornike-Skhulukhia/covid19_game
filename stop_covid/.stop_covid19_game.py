# import
import pygame
import random
import time
import numpy as np
import re

# define things
WIDTH = 320
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
        self.mass = (int(re.search(r'(\d{1,3})\.png',img).group(1)) // 2 )**3

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.update_x_width = self.rect.width + abs(self.speed_x)
        self.update_y_width = self.rect.height + abs(self.speed_y)


    def get_mass(self):
        return self.mass

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



# def main():        
enemies_num = 5
enemy_pics = [
                # 'img/enemy_16.png',
                'img/enemy_32.png',
                # 'img/enemy_48.png',
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

# enemies = [
#     Enemy(screen=screen, x=172, y=265, speed_x=1, speed_y=-8, img=enemy_pics[0], groups=ALL_SPRITES),
#     Enemy(screen=screen, x=218, y=232, speed_x=-7, speed_y=8, img=enemy_pics[0], groups=ALL_SPRITES),
# ]

ALL_SPRITES.add(enemies)

# GO
screen.fill(BG_COLOR)
pygame.display.update()


FPS = 30

run = 1
while run:
    pygame.time.wait(1000 // FPS)
    # time.sleep(1000 // FPS / 1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = 0

    screen.fill(BG_COLOR)

    # redraw enemies
    new_speeds = {}  # index of enemy --> new speed

    for index, enemy in enumerate(enemies):
        # screen.fill(BG_COLOR, enemy.rect)
        update_region = enemy.move()
        
        # pygame.display.update(update_region)

        # for enemy in enemies:
        # collisions

        # ALL_SPRITES.remove(enemy)
        collided = pygame.sprite.spritecollide(
                                            enemy,
                                            [i for i in ALL_SPRITES if i is not enemy],
                                            False,
                                            pygame.sprite.collide_mask)

        if collided:
            ob1 = enemy
            ob2 = collided[0]  # use first now

            print("object 1 initial speeds: ", ob1.get_speed_x(), ob1.get_speed_y())
            print("object 1 center positions: ", ob1.get_center_x(), ob1.get_center_y())
            print("object 2 initial speeds: ",ob2.get_speed_x(), ob2.get_speed_y())
            print("object 2 center positions: ", ob2.get_center_x(), ob2.get_center_y())

            # dist = np.sqrt((ob1.get_center_x() - ob2.get_center_x())**2 + (ob1.get_center_y() - ob2.get_center_y())**2)
            # print("dist:", dist)

            theta1 = np.arctan2(ob1.get_center_y(), ob1.get_center_x())
            theta2 = np.arctan2(ob2.get_center_y(), ob2.get_center_x())
            phi = np.arctan2(ob2.get_center_y() - ob1.get_center_y(), ob2.get_center_x() - ob1.get_center_x())
            m1, m2 = ob1.mass, ob2.mass
            v1 = np.sqrt(ob1.get_speed_x() * ob1.get_speed_x() + ob1.get_speed_y() * ob1.get_speed_y())
            v2 = np.sqrt(ob2.get_speed_x() * ob2.get_speed_x() + ob2.get_speed_y() * ob2.get_speed_y())

            dx1F = round((v1 * np.cos(theta1 - phi) * (m1-m2) + 2*m2*v2*np.cos(theta2 - phi)) / (m1+m2) * np.cos(phi) + v1*np.sin(theta1-phi) * np.cos(phi+np.pi/2) ,0)
            dy1F = round((v1 * np.cos(theta1 - phi) * (m1-m2) + 2*m2*v2*np.cos(theta2 - phi)) / (m1+m2) * np.sin(phi) + v1*np.sin(theta1-phi) * np.sin(phi+np.pi/2) ,0)

            dx2F = round((v2 * np.cos(theta2 - phi) * (m2-m1) + 2*m1*v1*np.cos(theta1 - phi)) / (m1+m2) * np.cos(phi) + v2*np.sin(theta2-phi) * np.cos(phi+np.pi/2) ,0)
            dy2F = round((v2 * np.cos(theta2 - phi) * (m2-m1) + 2*m1*v1*np.cos(theta1 - phi)) / (m1+m2) * np.sin(phi) + v2*np.sin(theta2-phi) * np.sin(phi+np.pi/2) ,0)

            print("object 1 final speeds: ", dx1F, dy1F)
            print("object 2 final speeds: ", dx2F, dy2F)
            new_speeds[index] = [dx1F, dy1F]
            
            # ob1.set_speed(dx1F, dy1F)
            # ob2.set_speed(dx2F, dy2F)
            # breakpoint()

            # enemy.reverse_y_speed()
            # enemy.reverse_x_speed()
            # break

    for index, new_speed in new_speeds.items():
        # if index % 2 == 0: new_speed[0] *= -1
        # if index % 2 != 0: new_speed[1] *= -1

        enemies[index].set_speed(*new_speed)

    # ALL_SPRITES.add(enemy)


    pygame.display.update()
    # redraw player

pygame.quit()


# if __name__ == '__main__':
#     main()
# 
