import pygame, sys, time, random
pygame.init()

size = width, height = 420, 270
speed = 2 * [ 1 ]
# BG_COLOR = 0,0,0
BG_COLOR = 0,0,0

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game 1')


# ballrect = ball.get_rect()
ballrect = pygame.Rect(0, 0, 24, 24)

COLOR = (255, 255, 55)

def get_random_color():
    return random.sample(range(1, 256, 10), 3)


while 1:
    time.sleep(0.01)
    # pygame.time.delay(3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
        COLOR = get_random_color()
        # speed[0] += random.randint(1, 5)

    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
        COLOR = get_random_color()

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, COLOR, ballrect)
    pygame.display.flip()

