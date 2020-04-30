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

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


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
                                    'shield': 'img/facemask_emoji_32.png',
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
                        'shield': 0,
                        }[self.mode]
        self.speed_y = {
                        'red': -random.randint(1, 20),
                        'green': -random.randint(1, 25),
                        'aliens': -random.randint(1, 15),
                        'aliens_red': -random.randint(1, 15),
                        'aliens_live': -random.randint(1, 15),
                        'toilet_paper': -random.randint(1, 10),
                        'shield': 0,
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
                 health=100,
                 level=1,
                 remaining_shield_time=5,
                 spaceship='primary',
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
        self.current_level = level
        self.health = health

        self.created_time = time.time()
        # self.shield_activated_at = False
        self.remaining_shield_time = remaining_shield_time


    def change_shoot_mode(self, new_mode):
        # primary - normal
        # also available red, green ...
        self.shoot_mode = new_mode


    def draw_meta_infobar(self):
        global HEIGHT, WIDTH, INFOBAR_HEIGHT

        font = pg.font.Font(None, 36)

        info_line_text = (
                     f'|   Score: {self.score}   '
                     f'|   Level: {self.current_level}   '
                     f'|   Life: {self.health}   '
                     f'|   Shield: {self.remaining_shield_time:.2f}   |'
                    )

        text = font.render(info_line_text, 1, (255, 255, 255))

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

        # self.recalculate_remaining_shield_time()
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
                                    enemies=self.enemies)
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

    def decrease_shield_time_by(self, ms):
        # if self.shield_activated_at is not False:    
        # self.remaining_shield_time -= 
        if self.shoot_mode == 'shield':
            self.remaining_shield_time -= ms / 1000

        if self.remaining_shield_time <= 0:
            self.remaining_shield_time = 0
            self.remove_shield()


    def activate_shield(self):
        # if time.time() - self.shield_activated_at < 10: return # use 10 secs
        if self.remaining_shield_time <= 0: return

        self.change_shoot_mode("shield")
        # self.shield_activated_at = time.time()

        for i in range(8):
            shield_bullet = BulletCircular(
                                mode=self.shoot_mode,  # shield
                                screen=self.screen,
                                x=100,
                                y=100,
                                player=self,
                                enemies=self.enemies)
            self.visible_bullets.append(shield_bullet)
        self.last_shoot_time += time.time() + 999_999_999


    def remove_shield(self):
        for i in [i for i in self.visible_bullets if isinstance(i, BulletCircular) and i.mode == "shield"]:
            self.visible_bullets.remove(i)

        self.change_shoot_mode('primary')
        self.last_shoot_time = time.time() - 999
        # self.shield_activated_at = 0


    def make_enemies_slooooooowww(self):
        for i in self.enemies:
            i.set_speed(
                        max(1, i.get_speed_x() // 2),
                        max(1, i.get_speed_y() // 2))

    def make_enemies_fast(self):
        for i in self.enemies:
            i.set_speed(
                        min(i.get_speed_x() * 2, 150),
                        min(i.get_speed_y() * 2, 150))



    def handle_collision(self):
        global ENEMY_SPRITES

        collided = pg.sprite.spritecollide(
                                            self,
                                            ENEMY_SPRITES,
                                            False,
                                            pg.sprite.collide_mask)
        if collided: self.health -= 1


    def move_me_and_my_bullets(self, pressed_keys=None):
        '''
        including bullets
        '''
        if pressed_keys[pg.K_UP]: self.increase_y_pos(-self.speed)
        if pressed_keys[pg.K_DOWN]: self.increase_y_pos(self.speed)
        if pressed_keys[pg.K_LEFT]: self.increase_x_pos(-self.speed)
        if pressed_keys[pg.K_RIGHT]: self.increase_x_pos(self.speed)
        if pressed_keys[pg.K_SPACE]: self.shoot()

        # temporary for testing
        if pressed_keys[pg.K_r]: self.remove_shield()
        if pressed_keys[pg.K_a]: self.activate_shield()
        if pressed_keys[pg.K_f]: self.make_enemies_fast()
        if pressed_keys[pg.K_s]: self.make_enemies_slooooooowww()


        # bullets
        shields_num = 1
        info = {}

        for index, bullet in enumerate(self.visible_bullets):
            if not isinstance(bullet, BulletCircular) or bullet.mode != "shield":
                if not bullet.move():
                    self.visible_bullets.pop(index)
            else:
                # print(len(self.visible_bullets))
                if shields_num == 1:
                    info[shields_num] = [self.rect.x + self.rect.width // 2 - 16,
                                        self.rect.y - 32 - 32]
                elif shields_num == 2:
                    info[shields_num] = [self.rect.x + self.rect.width + 32,
                                        self.rect.y + self.rect.height // 2 - 16]
                elif shields_num == 3:
                    info[shields_num] = [self.rect.x + self.rect.width // 2 - 16,
                                        self.rect.y + self.rect.height + 32]
                elif shields_num == 4:
                    info[shields_num] = [self.rect.x - 32 - 32,
                                        self.rect.y + self.rect.height // 2 - 16]
                elif shields_num == 5:
                    info[shields_num] = [
                                        (info[1][0] + info[2][0] ) // 2,
                                        (info[1][1] + info[2][1] ) // 2,
                                        ]
                elif shields_num == 6:
                    info[shields_num] = [
                                        (info[2][0] + info[3][0] ) // 2,
                                        (info[2][1] + info[3][1] ) // 2,
                                        ]
                elif shields_num == 7:
                    info[shields_num] = [
                                        (info[3][0] + info[4][0] ) // 2,
                                        (info[3][1] + info[4][1] ) // 2,
                                        ]
                elif shields_num == 8:
                    info[shields_num] = [
                                        (info[4][0] + info[1][0] ) // 2,
                                        (info[4][1] + info[1][1] ) // 2,
                                        ]
                else:
                    continue   # bug ?

                bullet.set_position(*info[shields_num])

                bullet.handle_enemies_collision()
                bullet.draw()
                shields_num += 1

        # health
        self.handle_collision()
        self.draw()

######################################

# define things
WIDTH = 984
HEIGHT = 576
INFOBAR_HEIGHT = 50
FPS = 30
ONE_FRAME_DURATION = 1000 // FPS

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

def get_enemies_for_level(level, enemy_sprites):
    global screen

    # if level < 3:
    enemies_num =  1 # 1 + level

    enemy_pics = [
                    'img/enemy_16.png',
                    'img/enemy_32.png',
                    'img/enemy_48.png',
                    'img/enemy_64.png',
                    'img/enemy_84.png',
                ] * (enemies_num // 5 + 3)

    enemies = [
                Enemy(
                    screen=screen,
                    x=random.choice(range(WIDTH)),
                    y=random.choice(range(HEIGHT - 200)),
                    speed_x=0, #random.randint(1, 3 + level),
                    speed_y=random.randint(1, 3 + level),
                    # img=enemy_pics[i],
                    img=img,
                    groups=enemy_sprites,
                    )
                for i, img in zip(range(enemies_num), random.sample(enemy_pics, enemies_num))]
    return enemies


def get_player_for_level(level, enemies, health=100, score=0):
    global screen

    # here we may add health & scores for specific round completions

    # if level  3:
    player = Player(screen=screen,
                    enemies=enemies,
                    speed=8 + (level // 5) * 2,
                    health=health,
                    score=score,
                    bullet_speed=15 + (level // 5) * 5,
                    shoot_interval=0.2,    # shoot mode will be primary, here we just test different things working
                    # shoot_mode= ['primary', 'red', 'green', 'aliens', 'aliens_red', 'aliens_live', 'toilet_paper'][(level - 1) % 7],
                    shoot_mode='primary',
                    level=level,   # very basic logic yet
                    spaceship=['primary', 'shuttle', 'scifi_blue', 'ferrari', 'tesla'][(level - 1) % 5],
                    )
    return player



# LET THE GAME BEGIN
ENEMY_SPRITES = pg.sprite.Group()

enemies = get_enemies_for_level(1, enemy_sprites=ENEMY_SPRITES)
player = get_player_for_level(1, enemies=enemies)

ENEMY_SPRITES.add(enemies)

run = 1


while run:
    #############################################
    pg.time.wait(ONE_FRAME_DURATION)
    # time.sleep(1000 // FPS / 1000)

    # EXIT
    for event in pg.event.get():
        if event.type == pg.QUIT: run = 0

    # UPDATE
    screen.fill(BG_COLOR)
    #############################################

    # ENEMIES
    for index, enemy in enumerate(enemies):
        enemy.move()
        for enemy_2 in enemies[index + 1:]:
            enemy.collide(enemy_2)

    # PLAYER
    player.move_me_and_my_bullets(pressed_keys=pg.key.get_pressed())
    player.decrease_shield_time_by(ONE_FRAME_DURATION)  # if necessary
    if player.health <= 0:
        print('Game Over, try again...')
        run = False

    if not player.enemies:
        # update info and start new round
        print(f'Round {player.current_level} Completed, Cool!...')

        ENEMY_SPRITES = pg.sprite.Group()
        enemies = get_enemies_for_level(level=player.current_level + 1, enemy_sprites=ENEMY_SPRITES)
        player = get_player_for_level(level=player.current_level + 1,
                                      enemies=enemies,
                                      health=player.health,
                                      score=player.score)

        ENEMY_SPRITES.add(enemies)

        # run = False
        # time.sleep(10)

    #############################################
    # SCREEN
    pg.display.update()

pg.quit()


# if __name__ == '__main__':
#     main()
# 
