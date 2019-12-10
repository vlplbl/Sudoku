''' Creating the board tiles '''
import pygame as pg
from settings import *


class Tile:
    def __init__(self, game, x, y):
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (self.rect.x//TILESIZE, self.rect.y//TILESIZE)
        self.solved = False
        self.selected = False
        self.generated = False
        self.number = ""

    def initial_draw(self):
        draw_text(self.image, BLACK, self.game.font, self.number)
        self.game.screen.blit(self.image, self.rect)
        pg.draw.rect(self.game.screen, BLACK, self.rect, 1)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        pg.draw.rect(self.game.screen, BLACK, self.rect, 1)
        # this check is for the solve button
        if not self.generated:
            self.image.fill(WHITE)
            draw_text(self.image, GREEN, self.game.font, self.number)
        else:
            self.image.fill(WHITE)
            draw_text(self.image, BLACK, self.game.font, self.number)
    

def draw_text(screen, color, font, num=" ", x=17, y=0, size=50):
    font = pg.font.Font(font, size)
    surf = font.render(str(num), 1, color)
    rect = surf.get_rect()
    screen.blit(surf, (x, y, rect.width, rect.height))


def draw_button(screen, text, color1, color2, pos_x, pos_y, w, h, font, func=None):
    font = pg.font.Font(font, 25)
    surf = font.render(text, 1, BLACK)
    rect = surf.get_rect()
    rect.center = ((pos_x+(w/2)), (pos_y+(h/2)))
    frame_rect = pg.Rect(pos_x, pos_y, w, h)
    pg.draw.rect(screen, color1, frame_rect)
    click = pg.mouse.get_pressed()
    if frame_rect.collidepoint(pg.mouse.get_pos()):
        pg.draw.rect(screen, color2, frame_rect)
        if click[0] and func:
            func()
    pg.draw.rect(screen, BLACK, frame_rect, 2)
    screen.blit(surf, rect)
