# from stop_covid19_game import *
import pygame as pg


#####################
# WIDTH = 984
# HEIGHT = 576
# INFOBAR_HEIGHT = 50
# FPS = 30
# ONE_FRAME_DURATION = 1000 // FPS

# SCREEN_SIZE = (WIDTH, HEIGHT + INFOBAR_HEIGHT)
# BG_COLOR = (255, 255, 255)

# # initialize
# pg.display.init()
# pg.font.init()

# screen = pg.display.set_mode(SCREEN_SIZE)
# screen.fill(BG_COLOR)
# pg.display.update()
# #####################


class Button:
    '''
    helper class for buttons
    '''
    def __init__(self,    screen,  color,   x,   y,
                 width,   height,  text=None,
                 text_color=None,  text_size=30):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color or (255, 0, 0)
        self.text_size = text_size
        self.drawn = False

    def draw(self):
        pg.draw.rect(
                    self.screen,
                    self.color,
                    (self.x, self.y, self.width, self.height), 0)
        if self.text:
            font = pg.font.Font(None, self.text_size)
            text = font.render(self.text, 1, (self.text_color))
            
            text_rect = text.get_rect()
            text_rect.left = self.x
            text_rect.top = self.y

            self.screen.blit(text, text_rect)
        self.drawn = True


    def is_hovered(self, mouse_pos):
        if not self.drawn: return False

        res = all([
                    self.x <= mouse_pos[0] <= self.x + self.width,
                    self.y <= mouse_pos[1] <= self.y + self.height
                    ])
        return res


    def is_clicked(self, mouse_pos, left_click):
        if left_click:
            return self.is_hovered(mouse_pos)


# # test
# btn = Button(screen, (255, 255, 0), 100, 100, 100, 100)
# btn.draw()
# pg.display.update()

# while True:
#     time.sleep(0.03)
#     for event in pg.event.get():
#         if event.type == pg.QUIT: run = 0

# pg.quit()
