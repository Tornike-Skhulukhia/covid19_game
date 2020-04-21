import sys
import pygame as pg
from pygame.math import Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((120, 60))
        self.image.fill(pg.Color('dodgerblue'))
        self.rect = self.image.get_rect(center=pos)


class Enemy(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((120, 60))
        self.image.fill(pg.Color('sienna1'))
        self.rect = self.image.get_rect(center=pos)


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    enemy_group = pg.sprite.Group(Enemy((200, 250)), Enemy((350, 250)))
    all_sprites.add(enemy_group)
    player = Player((100, 300), all_sprites)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEMOTION:
                player.rect.center = event.pos

        all_sprites.update()
        # Check which enemies collided with the player.
        # spritecollide returns a list of the collided sprites.
        collided_enemies = pg.sprite.spritecollide(player, enemy_group, False)

        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        for enemy in collided_enemies:
            # Draw rects around the collided enemies.
            pg.draw.rect(screen, (0, 190, 120), enemy.rect, 4)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()