import pygame, sys, time
pygame.init()

size = width, height = 480, 720
speed = 2 * [ 1 ]
# black = 0,0,0
black = 40,0,0

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game 1')
ball = pygame.image.load('small_ball.png')
ballrect = ball.get_rect()



while 1:
    time.sleep(0.01)
    # pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
