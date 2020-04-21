# import
import pygame
import random
import time

# define things
WIDTH = 720
HEIGHT = 480
SCREEN_SIZE = (WIDTH, HEIGHT)
BG_COLOR = (20, 20, 20)

# initialize
pygame.display.init()

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

WALL_HIT_SOUND = pygame.mixer.Sound('audio/basic_fist_hit.wav')

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
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.img)

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.update_x_width = self.rect.width + abs(self.speed_x)
        self.update_y_width = self.rect.height + abs(self.speed_y)


    def increase_speed_by(self, x_num, y_num):
        self.speed_x += x_num
        self.speed_y += y_num

        # update rectangles for updates
        self.update_x_width = self.rect.width + abs(self.speed_x)
        self.update_y_width = self.rect.height + abs(self.speed_y)

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

        # x, y, width, height
        # if random.randint(1, 4) == 2: breakpoint()

        # X
        # update_region[0] += -self.speed_x

        update_region = [
                        [new_x, self.rect.x][self.speed_x > 0] ,
                        [new_y, self.rect.y][self.speed_y > 0] ,
                        self.update_x_width,
                        self.update_y_width
                        ]

        # update_region = self.rect[:]
        # update_region[2] += self.speed_x
        # update_region[3] += self.speed_y

        # Y
        # update_region[1] += -self.speed_y

        # screen borders
        if not 0 <= new_x <= (WIDTH - self.rect.width):
            # breakpoint()
            new_x = min(new_x, WIDTH - self.rect.width)
            new_x = max(new_x, 0)
            # print('X collided')
            self.reverse_x_speed()

        if not 0 <= new_y <= (HEIGHT - self.rect.height):
            # breakpoint()
            new_y = min(new_y, HEIGHT - self.rect.height)
            new_y = max(new_y, 0)
            # print('Y collided')
            self.reverse_y_speed()

        self.rect.x = new_x
        self.rect.y = new_y
        # print('New positions:     ', list(self.rect))

        self.draw()

        
        # print('Update this region:', update_region)
        return update_region


# def main():        
enemies_num = 4
enemy_pics = [
                'img/enemy_48.png',
                # 'img/enemy_64.png',
                # 'img/enemy_84.png',
                # 'img/enemy_84.png',
            ] * enemies_num


ALL_SPRITES = pygame.sprite.Group()

enemies = [
            Enemy(
                screen=screen,
                x=random.choice(range(WIDTH)),
                y=random.choice(range(HEIGHT)),
                speed_x=random.randint(1, 3),
                speed_y=random.randint(1, 3),
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = 0

    # redraw enemies
    for enemy in enemies:
        screen.fill(BG_COLOR, enemy.rect)
        update_region = enemy.move()
        
        pygame.display.update(update_region)

        # collisions
        ALL_SPRITES.remove(enemy)
        collided = pygame.sprite.spritecollide(enemy, ALL_SPRITES, False, pygame.sprite.collide_mask)

        if collided:
            # [enemy.reverse_y_speed,enemy.reverse_x_speed][random.choice([0, 1])]()
            enemy.reverse_y_speed()
            enemy.reverse_x_speed()
            
            enemy.increase_speed_by(1, 1)
            print('speed increased by 1x1')
            # breakpoint()

        ALL_SPRITES.add(enemy)


    # redraw player

pygame.quit()


# if __name__ == '__main__':
#     main()
# 
