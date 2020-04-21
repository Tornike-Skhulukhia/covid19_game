import pygame, sys, time
import random

pygame.init()

# ball = pygame.image.load('small_ball.png')
# ballrect = ball.get_rect()

ballrect = pygame.Rect(0, 0, 30, 30)


size = width, height = 480, 720
# black = 0,0,0
black = 40,0,0



RAND_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

speed = 1

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game 1')
ball = pygame.image.load('small_ball.png')
ballrect = ball.get_rect()

x = y = 1
obj_width = 24
obj_height = 24



obj_color = random.choice(RAND_COLORS)

run = True
while run:
    # time.sleep(0.01)
    # pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]: ballrect.x -= speed
    if keys[pygame.K_RIGHT]: ballrect.x += speed
    if keys[pygame.K_UP]: ballrect.y -= speed
    if keys[pygame.K_DOWN]: ballrect.y += speed

    screen.fill(black)
    pygame.draw.rect(screen, obj_color, (x, y, obj_width, obj_height))
    screen.blit(ball, ballrect)
    pygame.display.update()

pygame.quit()

