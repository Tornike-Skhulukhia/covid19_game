# import
import pygame as pg
import random
import time
import numpy as np
import re
import math
######################################

class Enemy(pg.sprite.Sprite):
    '''
        defines enemies class
    '''
    def __init__(self, screen, img='img/enemy_48.png', speed_x=2, speed_y=2, x=0, y=0, groups=[]):
        super().__init__(*groups)
        self.screen = screen
        # self.img = pg.image.load(img)
        self.img = pg.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.img)
        self.radius = int(re.search(r'(\d{1,3})\.png',img).group(1)) // 2 

        self.speed_x = speed_x
        self.speed_y = speed_y


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

    def set_x_pos(self, x):
        self.rect.x = x

    def set_y_pos(self, y):
        self.rect.y = y

    def get_x_pos(self):
        return self.rect.x

    def get_y_pos(self):
        return self.rect.y

    def set_speed(self, x_num, y_num):
        self.speed_x = x_num
        self.speed_y = y_num


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
        '''
        move to current direction
        '''
        global WIDTH, HEIGHT

        new_x = self.get_x_pos() + self.get_speed_x()
        new_y = self.get_y_pos() + self.get_speed_y()

        # screen borders
        if not 0 <= new_x <= (WIDTH - self.rect.width):
            new_x = min(new_x, WIDTH - self.rect.width)
            new_x = max(new_x, 0)
            self.reverse_x_speed()

        if not 0 <= new_y <= (HEIGHT - self.rect.height):
            new_y = min(new_y, HEIGHT - self.rect.height)
            new_y = max(new_y, 0)
            self.reverse_y_speed()

        self.set_x_pos(new_x)
        self.set_y_pos(new_y)

        self.draw()


    def collide(self, other):
        '''
        update speeds if collision happens
        '''
        dx = self.get_center_x() - other.get_center_x()
        dy = self.get_center_y() - other.get_center_y()

        distance = math.hypot(dx, dy)

        if distance < self.radius + other.radius:
            tangent = math.atan2(dy, dx)

            angle_1 = np.arctan2(self.get_center_y(), self.get_center_x())
            angle_2 = np.arctan2(other.get_center_y(), other.get_center_x())

            speed_1 = (self.get_speed_x(), self.get_speed_y())
            speed_2 = (other.get_speed_x(), other.get_speed_y())
            self.set_speed(*speed_2)
            other.set_speed(*speed_1)

            # correction
            angle = 0.5 * math.pi + tangent
            self.set_center(self.get_center_x() + math.sin(angle), self.get_center_y() - math.cos(angle))
            other.set_center(other.get_center_x() - math.sin(angle), other.get_center_y() + math.cos(angle))



class Bullet:
    '''
        defines bullet class
    '''
    def __init__(self, screen, x, y, player, enemies, img='img/bullet_32.png', speed=20):
        self.screen = screen
        self.img = pg.image.load(img)
        self.mask = pg.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.enemies = enemies
        self.player = player

    def draw(self):
        self.screen.blit(self.img, self.rect)

    def handle_enemies_collision(self):
        global ENEMY_SPRITES
        # new method
        collided = pg.sprite.spritecollide(
                                            self,
                                            ENEMY_SPRITES,
                                            False,
                                            pg.sprite.collide_mask)
        for enemy in collided:
            self.enemies.remove(enemy)
            ENEMY_SPRITES.remove(enemy)
            self.player.score += 1

    def move(self):
        self.rect.y -= self.speed
        self.handle_enemies_collision()
        self.draw()
        # True if still visible
        return (self.rect.y - self.rect.height) > -20 



class BulletCircular(Bullet):
    def __init__(self, mode, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # breakpoint()
        self.mode = mode
        self.img = pg.image.load({
                                    'red': 'img/circular_bullet_red_48.png',
                                    'green': 'img/circular_bullet_green_48.png',
                                    'aliens': 'img/aliens_round_spaceship_48.png',
                                    'aliens_red': 'img/red_rounded_aliens_plate_48.png',
                                    'aliens_live': 'img/alien_live_48.png',
                                    'toilet_paper': 'img/toilet_paper_48.png',
                                    # 'blue': 'img/circular_bullet_red_48.png',
                                }[self.mode])
        self.mask = pg.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        self.rect.x = kwargs['x']
        self.rect.y = kwargs['y']
        self.speed_x = {
                        'red': random.randint(-20, 20),
                        'green': random.randint(-35, 35),
                        'aliens': random.randint(-25, 25),
                        'aliens_red': random.randint(-25, 25),
                        'aliens_live': random.randint(-25, 25),
                        'toilet_paper': random.randint(-15, 15),
                        }[self.mode]
        self.speed_y = {
                        'red': -random.randint(1, 20),
                        'green': -random.randint(1, 25),
                        'aliens': -random.randint(1, 15),
                        'aliens_red': -random.randint(1, 15),
                        'aliens_live': -random.randint(1, 15),
                        'toilet_paper': -random.randint(1, 10),
                        }[self.mode]

    def move(self):
        '''
        Solve bug/s here later!!!
        '''
        global WIDTH, HEIGHT
        # breakpoint()
        new_x = self.rect.x + self.speed_x
        new_y = self.rect.y + self.speed_y

        # breakpoint()
        # screen borders
        if not 0 <= new_x <= (WIDTH - self.rect.width):
            new_x = min(new_x, WIDTH - self.rect.width)
            new_x = max(new_x, 0)
            self.speed_x = -self.speed_x

        if not 0 <= new_y <= (HEIGHT - self.rect.height):
            new_y = min(new_y, HEIGHT - self.rect.height)
            new_y = max(new_y, 0)
            self.speed_y = - self.speed_y

        self.rect.x = new_x
        self.rect.y = new_y

        self.handle_enemies_collision()
        self.draw()
        # True until bullet on screen
        return (self.rect.y - self.rect.height) > -18


class Player:
    '''
    defines player class
    '''
    def __init__(self,
                 screen,
                 enemies,
                 speed=5,
                 shoot_interval=0.5,
                 shoot_mode='primary',
                 bullet_speed=10,
                 score=0,
                 life=100,
                 level=1,

                 spaceship='',
                 ):
        global WIDTH, HEIGHT

        self.screen = screen
        self.spaceship = spaceship 
        self.img = pg.image.load({
                                'primary':'img/spaceship_64.png',
                                'shuttle':'img/shuttle_76.png',
                                'scifi_blue':'img/spacecraft_blue_76.png',
                                'ferrari':'img/ferrari_92.png',
                                'tesla':'img/tesla_92.png',
                                }[self.spaceship])

        self.mask = pg.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        self.rect.x = WIDTH // 2 - (self.rect.width / 2)
        self.rect.y = HEIGHT - (self.rect.height + 10)
        self.speed = speed

        # for wall collision
        self.min_left_pos = 0
        self.max_right_pos = WIDTH - self.rect.width 
        self.min_up_pos = 0
        self.max_down_pos = HEIGHT - self.rect.height 

        self.bullet_speed = bullet_speed
        self.shoot_interval = shoot_interval  # min time to shoot next
        self.shoot_mode = shoot_mode
        self.last_shoot_time = 0
        self.visible_bullets = []
        self.used_bullets_num = 0

        self.enemies = enemies

        self.score = score
        self.level = level
        self.life = life

        self.created_time = time.time()


    def change_shoot_mode(self, new_mode):
        # primary - normal
        # also available red, green ...
        self.shoot_mode = new_mode

    def draw_meta_infobar(self):
        global HEIGHT, WIDTH, INFOBAR_HEIGHT

        font = pg.font.Font(None, 36)
        text = font.render(
                        f'|   Score: {self.score}   |   Level: {self.level}   |   Life: {self.life}   |',
                        1, 
                        (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = WIDTH / 2
        textpos.centery = HEIGHT + 15
        # textpos.centerx = self.screen.get_rect().centerx
        self.screen.blit(text, textpos)


    def draw(self):
        '''
        draw player and meta infobar
        '''
        self.screen.blit(self.img, self.rect)
        self.draw_meta_infobar()


    def increase_x_pos(self, delta_x):
        new_x = self.rect.x + delta_x

        if self.min_left_pos <= new_x <= self.max_right_pos:
            self.rect.x = new_x


    def increase_y_pos(self, delta_y):
        new_y = self.rect.y + delta_y

        if self.min_up_pos <= new_y <= self.max_down_pos:
            self.rect.y = new_y


    def bullet_is_ready(self):
        return time.time() - self.last_shoot_time >= self.shoot_interval


    def shoot(self):
        if self.bullet_is_ready():
            # breakpoint()
            if self.shoot_mode != 'primary':
                new_bullet = BulletCircular(
                                    mode=self.shoot_mode,  # red, green...
                                    screen=self.screen,
                                    x=self.rect.center[0] - 16,
                                    y=self.rect.center[1],
                                    player=self,
                                    enemies=self.enemies,
                                    speed=self.bullet_speed)
            else:
                new_bullet = Bullet(screen=self.screen,
                                    x=self.rect.center[0] - 16,
                                    y=self.rect.center[1],
                                    player=self,
                                    enemies=self.enemies)
            self.visible_bullets.append(new_bullet)
            # print('Fire!')
            self.last_shoot_time = time.time()
            self.used_bullets_num += 1
            # print(self.used_bullets_num)

    def handle_collision(self):
        global ENEMY_SPRITES

        collided = pg.sprite.spritecollide(
                                            self,
                                            ENEMY_SPRITES,
                                            False,
                                            pg.sprite.collide_mask)
        if collided: self.life -= 1


    def move_me_and_my_bullets(self, pressed_keys=None):
        '''
        including bullets
        '''
        if pressed_keys[pg.K_UP]: self.increase_y_pos(-self.speed)
        if pressed_keys[pg.K_DOWN]: self.increase_y_pos(self.speed)
        if pressed_keys[pg.K_LEFT]: self.increase_x_pos(-self.speed)
        if pressed_keys[pg.K_RIGHT]: self.increase_x_pos(self.speed)
        if pressed_keys[pg.K_SPACE]: self.shoot()

        # bullets
        for index, bullet in enumerate(self.visible_bullets):
            if not bullet.move():
                self.visible_bullets.pop(index)

        # health
        self.handle_collision()
        self.draw()

######################################

# define things
WIDTH = 984
HEIGHT = 576
INFOBAR_HEIGHT = 50
FPS = 30

SCREEN_SIZE = (WIDTH, HEIGHT + INFOBAR_HEIGHT)
BG_COLOR = (20, 20, 20)


# initialize
pg.display.init()
pg.font.init()

# pg.mixer.pre_init(44100, -16, 1, 512)
# pg.mixer.init()

screen = pg.display.set_mode(SCREEN_SIZE)

# GO
screen.fill(BG_COLOR)
pg.display.update()

# WALL_HIT_SOUND = pg.mixer.Sound('audio/basic_fist_hit.wav')

ICON = pg.image.load('img/enemy_100px.png')
pg.display.set_icon(ICON)
pg.display.set_caption("StopCovid19")


# def main():        
enemies_num = 20
enemy_pics = [
                'img/enemy_16.png',
                # 'img/enemy_32.png',
                # 'img/enemy_48.png',
                # 'img/enemy_64.png',
                # 'img/enemy_84.png',
                # 'img/enemy_84.png',
                'img/enemy_84.png',
            ] * enemies_num


ENEMY_SPRITES = pg.sprite.Group()

ENEMIES = [
            Enemy(
                screen=screen,
                # x=random.choice(range((WIDTH // enemies_num) *i, (WIDTH // enemies_num)  * (i+1))),
                # y=random.choice(range((HEIGHT // enemies_num) *i, (HEIGHT // enemies_num)  * (i+1))),
                x=random.choice(range(WIDTH)),
                y=random.choice(range(HEIGHT - 200)),
                speed_x=random.randint(1, 3),
                speed_y=random.randint(1, 3),
                img=enemy_pics[i],
                groups=ENEMY_SPRITES,
                )
            for i in range(enemies_num)]

ENEMY_SPRITES.add(ENEMIES)

player = Player(screen=screen,
                enemies=ENEMIES,
                speed=8,
                bullet_speed=15,
                shoot_interval=0.2,
                shoot_mode='primary',
                # shoot_mode
                spaceship='primary',
                )

run = 1
while run:
    pg.time.wait(1000 // FPS)
    # time.sleep(1000 // FPS / 1000)

    # EXIT
    for event in pg.event.get():
        if event.type == pg.QUIT: run = 0

    # UPDATE
    screen.fill(BG_COLOR)

    # ENEMIES
    for index, enemy in enumerate(ENEMIES):
        enemy.move()
        for enemy_2 in ENEMIES[index + 1:]:
            enemy.collide(enemy_2)

    # PLAYER
    player.move_me_and_my_bullets(pressed_keys=pg.key.get_pressed())
    if player.life <= 0:
        print('Game Over, try again...')
        run = False

    if not player.enemies:
        print('Round 1 Completed, to be continued soon...')
        run = False
        # time.sleep(10)
    # SCREEN
    pg.display.update()

pg.quit()


# if __name__ == '__main__':
#     main()
# 
