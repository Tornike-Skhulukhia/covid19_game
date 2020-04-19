import pygame
import random
import time

WIDTH = 720
HEIGHT = 480
SCREEN_SIZE = (WIDTH, HEIGHT)
BG_COLOR = (0, 0, 0)

pygame.display.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

# ICON = pygame.image.load('enemy_100px.png')
# pygame.display.set_icon(ICON)
# pygame.display.set_caption("StopCovid19")

class Enemy:
    def __init__(self, screen, img='enemy_100px.png', speed=2, x=0, y=0):
        self.screen = screen
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

        self.direction = 1  # moves to right , -1 - left
        # breakpoint()


    def draw(self):
        self.screen.blit(self.img, self.rect)


    def move(self):
        '''move to current direction'''
        global WIDTH, HEIGHT

        new_x = self.rect.x + self.direction * self.speed

        update_region = self.rect[:]
        update_region[0] += self.speed * -self.direction
        update_region[2] += update_region[3] + self.speed

        if not 0 <= new_x <= (WIDTH - self.rect.width):
            new_x = min(new_x, WIDTH - self.rect.width)
            new_x = max(new_x, 0)

            # print('direction changed')
            self.direction *= -1

        # print(new_x)
        self.rect.x = new_x

        self.draw()

        return update_region



    # def randomly_move(self): 
    #     # get new position
    #     direction = random.choice([1, -1])
        
    #     new_x = self.rect.x + self.speed * direction
    #     self.rect.x = new_x

    #     # draw
    #     self.draw()



enemies_num = 3


enemies = [
            Enemy(
                screen=screen,
                x=random.randint(1, 6)*100,
                y=random.randint(1, 4)*100,
                speed=random.randint(1, 5))

            for i in range(enemies_num)]



run = 1
while run:
    # time.sleep(0.01)
    pygame.time.wait(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = 0

    for enemy in enemies:
        screen.fill(BG_COLOR, enemy.rect)
        update_region = enemy.move()

        pygame.display.update(update_region)


pygame.quit()
