# import
import pygame as pg
import random
import time
import numpy as np
import re
import math
from btn_temp import Button
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

        self.mode = mode
        self.img = pg.image.load({
                                    'red': 'img/circular_bullet_red_48.png',
                                    'green': 'img/circular_bullet_green_48.png',
                                    'aliens': 'img/aliens_round_spaceship_48.png',
                                    'aliens_red': 'img/red_rounded_aliens_plate_48.png',
                                    'aliens_live': 'img/alien_live_48.png',
                                    'toilet_paper': 'img/toilet_paper_48.png',
                                    'shield': 'img/facemask_emoji_32.png',
                                }[self.mode])
        self.mask = pg.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        self.rect.x = kwargs['x']
        self.rect.y = kwargs['y']
        self.speed_x = {
                        'red': random.randint(-20, 20),
                        'green': random.choice([-1, 1]) * random.randint(1, 50),
                        'aliens': random.randint(-25, 25),
                        'aliens_red': random.randint(-35, 35),
                        'aliens_live': random.randint(-30, 30),
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
        global WIDTH, HEIGHT
        new_x = self.rect.x + self.speed_x
        new_y = self.rect.y + self.speed_y

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
                 remaining_shield_time=3,
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

        self.enemies = enemies

        self.score = score
        self.current_level = level
        self.health = health

        self.creation_time = time.time()
        self.remaining_shield_time = remaining_shield_time
        self.gift = False
        self.gift_freq_sec = 7


    def change_shoot_mode(self, new_mode):
        # primary - normal
        # also available red, green ...
        self.shoot_mode = new_mode


    def get_shield_text_color(self):
        if self.remaining_shield_time >= 3:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        return color

    def get_life_text_color(self):
        if self.health > 50:
            color = (0, 255, 0)
        elif self.health > 30:
            color = (200, 2, 78)
        else:
            color = (255, 0, 0)
        return color

    def get_health_image(self):
        if self.health > 70:
            img_file = 'img/colorful_tree_40.png'
        elif self.health > 30:
            img_file = 'img/heart_tree_32.png'
        else:
            img_file = 'img/heart_32.png'
        return img_file

    def get_shield_image(self):
        if self.remaining_shield_time >= 2:
            img_file = 'img/facemask_red_48.png'
        elif self.remaining_shield_time >= 1:
            img_file = 'img/facemask_black_40.png'
        else:
            img_file = 'img/facemask_surgical_48.png'

        return img_file


    def get_gift_img(self):
        return {
            'slow_down': 'img/sloth_64.png',  # enemy
            'speed_up': 'img/lightning_mcqueen_76.png',    # player
            'red': 'img/transformers_logo_48.png',
            'green': 'img/hulk_42.png',
            'toilet_paper': 'img/towel_blue_76.png', 
            'aliens_live': 'img/galaxy_76.png',
            'aliens': 'img/galaxy_blue_64.png',
            'aliens_red': 'img/spaceship_silver_76.png',
        }.get(self.gift, 'img/gift_icon_48.png')


    def apply_gift(self, gift):
        if gift == 'slow_down':
            self.make_enemies_slooooooowww()
        elif gift == 'speed_up':
            self.make_enemies_fast()
        else:
            self.change_shoot_mode(gift)

        self.gift = gift



    def draw_meta_infobar(self):
        global HEIGHT, WIDTH, INFOBAR_HEIGHT


        font = pg.font.Font(None, 36)

        info_line_text = (
                     f'|   Score: {self.score}  |      '
                     f'|   Level: {self.current_level}   |'
                    )

        life_level_text = font.render(info_line_text, 1, (255, 255, 255))
        life_text = font.render(
                                f'|        : {self.health:^3}   |',
                                1,
                                self.get_life_text_color())
        shield_text = font.render(
                            f'|           : {self.remaining_shield_time:.2f}   |',
                            1,
                            self.get_shield_text_color())

        info_text_pos = life_level_text.get_rect()
        info_text_pos.centerx = WIDTH / 2 - 120
        info_text_pos.centery = HEIGHT + 15

        # gift image on left
        gift_img = pg.image.load(self.get_gift_img())
        gift_img_pos = gift_img.get_rect()
        gift_img_pos.left = 80
        gift_img_pos.centery = info_text_pos.centery

        gift_img_bottom_line = font.render('__________',
                                            1,
                                            {
                                                'speed_up': (230, 0, 0),
                                                False: (100, 100, 100)
                                            }.get(self.gift, (0, 230, 0)))

        gift_img_bottom_line_rect = gift_img_bottom_line.get_rect()
        gift_img_bottom_line_rect.left = 40
        gift_img_bottom_line_rect.centery = info_text_pos.centery + 18



        # life
        life_text_rect = life_text.get_rect()
        life_text_rect.right = info_text_pos.right + 185
        life_text_rect.centery = info_text_pos.centery

        life_img = pg.image.load(self.get_health_image())
        # life_img = pg.image.load('img/heart_32.png')
        life_img_rect = life_img.get_rect()
        life_img_rect.left = info_text_pos.right + 60
        life_img_rect.centery = info_text_pos.centery

        # shield
        shield_text_rect = shield_text.get_rect()
        shield_text_rect.right = info_text_pos.right + 400
        shield_text_rect.centery = info_text_pos.centery

        mask_img = pg.image.load(self.get_shield_image())
        mask_rect = mask_img.get_rect()
        mask_rect.left = info_text_pos.right + 240
        mask_rect.centery = info_text_pos.centery

        self.screen.blit(gift_img, gift_img_pos)
        self.screen.blit(gift_img_bottom_line, gift_img_bottom_line_rect)
        self.screen.blit(life_level_text, info_text_pos)
        self.screen.blit(life_img, life_img_rect)
        self.screen.blit(life_text, life_text_rect)
        self.screen.blit(mask_img, mask_rect)
        self.screen.blit(shield_text, shield_text_rect)


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
            # print('Fire!')  :)
            self.last_shoot_time = time.time()

    def decrease_shield_time_by(self, ms):
        if self.shoot_mode == 'shield':
            self.remaining_shield_time -= ms / 1000

            if self.remaining_shield_time <= 0:
                self.remaining_shield_time = 0
                self.remove_shield()


    def activate_shield(self):
        if self.remaining_shield_time <= 0: return

        self.change_shoot_mode("shield")
        self.reset_gift()

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
        self.last_shoot_time = time.time()


    def reset_gift(self):
        self.gift = False

    def make_enemies_slooooooowww(self):
        for i in self.enemies:
            i.set_speed(
                        max(1, i.get_speed_x() // 5),
                        max(1, i.get_speed_y() // 5))

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
        # if pressed_keys[pg.K_f]: self.make_enemies_fast()
        # if pressed_keys[pg.K_s]: self.make_enemies_slooooooowww()


        # bullets
        shields_num = 1
        info = {}

        for index, bullet in enumerate(self.visible_bullets):
            if not isinstance(bullet, BulletCircular) or bullet.mode != "shield":
                if not bullet.move():
                    self.visible_bullets.pop(index)
            else:
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


def get_enemies_for_level(level, enemy_sprites):
    global screen

    # if level < 3:
    enemies_num = min(200, 1 + (level if level < 10 else int(level * 1.5)))

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
                    speed_x=min(150, random.randint(3, 5 + (level * 2 if level < 15 else level * 3))),
                    speed_y=min(150, random.randint(3, 5 + (level * 2 if level < 15 else level * 3))),
                    # img=enemy_pics[i],
                    img=img,
                    groups=enemy_sprites,
                    )
                for i, img in zip(range(enemies_num), random.sample(enemy_pics, enemies_num))]
    return enemies


def get_spaceship_for(level):
    if level <= 5 or level % 11 == 0:
        spaceship = "primary"
    elif level <= 10:
        spaceship = 'ferrari'
    elif level <= 15:
        spaceship = 'shuttle'
    elif level <= 25 or level % 25 == 0:
        spaceship = 'tesla'
    else:
        spaceship = 'scifi_blue'
    return spaceship


def get_gift_for(level, gift_freq_sec):
    gift = 0

    if random.randint(1, FPS * gift_freq_sec) == 1:
        modes = ['speed_up']

        if level > 2:
            modes.append('slow_down')
        if level > 7:
            modes.append('aliens')
        if level > 12:
            modes.append('red')
        if level > 17:
            modes.append('aliens_live')
        if level > 22:
            modes.append('aliens_red')
        if level > 27:
            modes.append('green')
        if level > 32:
            modes.append('toilet_paper')

        gift = random.choice(modes)

    return gift



def get_player_for_level(level, enemies, health=100, score=0, remaining_shield_time=0, round_length=999):
    global screen

    # here we may add health & scores for specific round completions

    # if level  3:
    player = Player(screen=screen,
                    enemies=enemies,
                    speed=5 + (level // 5) * 2,
                    health=min(100, health + (level // 5) * 4),
                    score=score + int(remaining_shield_time*10) + (max(0, 30 - round_length) * level),
                    bullet_speed=10 + (level // 5) * 5,
                    shoot_interval=max(0.01, 0.5 - (level // 5) * 0.05),
                    shoot_mode='primary',
                    level=level,   # very basic logic yet
                    spaceship=get_spaceship_for(level),
                    )
    return player




def handle_welcome_screen(welcome_screen_info, score_save_resp):
    '''
    tells which button was pressed,
        start game, exit, or save score.
    '''
    global ONE_FRAME_DURATION, screen, BG_COLOR, WIDTH, HEIGHT
    last_score = welcome_screen_info['score']

    start_btn = Button(screen=screen,      color=BG_COLOR,           x=WIDTH // 2 - 175, 
                       y=HEIGHT//2-170,    width=380,                height=50,
                       text='Start Game',  text_color=(0, 255, 0),   text_size=100)

    exit_btn = Button(screen=screen,       color=BG_COLOR,           x=WIDTH // 2 - 50, 
                      y=HEIGHT//2,         width=140,                height=50,
                      text='Exit',         text_color=(255, 0, 0),   text_size=100)

    # draw last score button with saving option
    save_btn = Button(screen=screen,             color=BG_COLOR,     x=WIDTH // 2 - 100, 
                      y=HEIGHT//2 + 200,         width=235,          height=50,
                      text=f'Save Score ({last_score})',
                      text_color=(250, 0, 250),   text_size=50)

    # save response 
    save_resp_btn = Button(screen=screen,             color=BG_COLOR,              x=WIDTH // 2 - 190,
                           y=HEIGHT//2 + 300,         width=0,                     height=0,
                           text=score_save_resp,    text_color=(255, 255, 55),   text_size=35)

    while 1:
        pg.time.wait(ONE_FRAME_DURATION); pg.event.get()
        screen.fill(BG_COLOR)

        keys = pg.key.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]

        start_btn.draw()
        exit_btn.draw()
        if last_score > 0: save_btn.draw()
        if score_save_resp: save_resp_btn.draw()
        pg.display.update()

        if start_btn.is_clicked(mouse_pos, left_click) or keys[pg.K_s]:
            return 'start game'
        elif exit_btn.is_clicked(mouse_pos, left_click) or keys[pg.K_e]:
            return 'exit'
        elif save_btn.is_clicked(mouse_pos, left_click):
            return 'save'


def save_data_in_external_db(data):
    import requests

    url = 'https://uct.ge/projects/covid19_game/save_data/' 

    try:
        resp = requests.post(url, data)
        # success - True
        return bool(resp.json()['OK'])
    except:
        # Failure - False
        return False


def handle_score_saving(welcome_screen_info):

    # get input
    global BG_COLOR
    from pygame_text_input import TextInput

    text_input = TextInput(initial_string='What is your name? :) (press Enter to save)',
                           text_color=(255, 255, 255),
                           cursor_color=(0, 255, 0))

    while True:
        pg.time.wait(ONE_FRAME_DURATION)
        screen.fill(BG_COLOR); events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                return ''

        enter_clicked = text_input.update(events)
        if enter_clicked:
            if save_data_in_external_db({'score': welcome_screen_info['score'],
                                         'level': welcome_screen_info['level'],
                                         'player': text_input.get_text().strip()}):
                return 'Your Score Saved Successfully!'.center(len('There was an error, Please Try Later'))
            else:
                return 'There was an error, Please Try Later'

        screen.blit(text_input.get_surface(), (10, 10))
        pg.display.update()


def prepare_game_screen():
    '''
    prepare things for later parts
    '''
    # LET THE GAME BEGIN
    global screen, WIDTH, HEIGHT, \
           INFOBAR_HEIGHT, FPS, ONE_FRAME_DURATION,\
           SCREEN_SIZE, BG_COLOR

    WIDTH = 984
    HEIGHT = 576
    INFOBAR_HEIGHT = 50
    FPS = 30
    ONE_FRAME_DURATION = 1000 // FPS

    SCREEN_SIZE = (WIDTH, HEIGHT + INFOBAR_HEIGHT)
    BG_COLOR = (20, 20, 20)

    SHOW_START_SCREEN = True

    # initialize
    pg.display.init()
    pg.font.init()

    screen = pg.display.set_mode(SCREEN_SIZE)
    screen.fill(BG_COLOR)
    pg.display.update()

    pg.display.set_icon(pg.image.load('img/enemy_100px.png'))
    pg.display.set_caption("StopCovid19")


def play_game():
    '''
    start game, return only if exit was pressed, or health = 0.

    returns:
        {
            'score': score,
            'level': level,
        }
    '''
    global ENEMY_SPRITES, screen, WIDTH, HEIGHT, \
            INFOBAR_HEIGHT, FPS, ONE_FRAME_DURATION,\
            SCREEN_SIZE, BG_COLOR    

    ENEMY_SPRITES = pg.sprite.Group()

    enemies = get_enemies_for_level(1, enemy_sprites=ENEMY_SPRITES)
    player = get_player_for_level(1, enemies=enemies)

    ENEMY_SPRITES.add(enemies)

    while True:
        pg.time.wait(ONE_FRAME_DURATION)
        # EXIT
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return {
                    'score': player.score,
                    'level': player.current_level,
                    'finish_reason': 'quit',
                }

        # UPDATE
        screen.fill(BG_COLOR)

        # GIFT
        if (not player.gift) and (player.shoot_mode != 'shield'):
            gift = get_gift_for(player.current_level, player.gift_freq_sec)
            if gift:
                player.apply_gift(gift)


        # ENEMIES
        for index, enemy in enumerate(enemies):
            enemy.move()
            for enemy_2 in enemies[index + 1:]:
                enemy.collide(enemy_2)

        # PLAYER
        player.move_me_and_my_bullets(pressed_keys=pg.key.get_pressed())
        player.decrease_shield_time_by(ONE_FRAME_DURATION)  # if necessary
        if player.health <= 0:
            # print('Game Over, try again...')
            return {
                'score': player.score,
                'level': player.current_level,
                'finish_reason': 'game over',
            }

        # NEXT ROUND
        if not player.enemies:
            # print(f'Round {player.current_level} Completed, Cool!...')
            ENEMY_SPRITES = pg.sprite.Group()
            enemies = get_enemies_for_level(level=player.current_level + 1, enemy_sprites=ENEMY_SPRITES)
            player = get_player_for_level(level=player.current_level + 1,
                                          enemies=enemies,
                                          health=player.health,
                                          score=player.score,
                                          remaining_shield_time=player.remaining_shield_time,
                                          round_length=int(time.time() - player.creation_time))
            ENEMY_SPRITES.add(enemies)

        # SCREEN
        pg.display.update()


if __name__ == '__main__':
    prepare_game_screen()

    welcome_screen_info = {'score':0, 'level':0}
    score_save_resp = ''

    while True:
        # GAME ICON WAS CLICKED
        welcome_screen_answer = handle_welcome_screen(welcome_screen_info, score_save_resp)

        # RESTART GAME
        if welcome_screen_answer == 'start game':
            # returns only if health <= 0 or player pressed X button
            welcome_screen_info = play_game()
            score_save_resp = ''

        # EXIT
        elif welcome_screen_answer == 'exit':
            break
        # SAVE SCORE
        elif welcome_screen_answer == 'save':
            # return True or False, depending on saving status
            # print('saving')
            score_save_resp = handle_score_saving(welcome_screen_info)

            if score_save_resp.strip() == 'Your Score Saved Successfully!':
                welcome_screen_info['score'] = 0
    pg.quit()
