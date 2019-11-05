''' Game settings '''
import pygame as pg


TILESIZE = 64
WIDTH = TILESIZE * 9
HEIGHT = TILESIZE * 9 + 64
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (150, 150, 150)
GREY = (200, 200, 200)
GREEN = (0, 128, 0)
LIGHTGREEN = (0, 255, 0)
YELLOW = (128, 128, 0)
LIGHTYELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LIGHTRED = (255, 0, 0)
RED = (128, 0, 0)

INPUT1 = [pg.K_1, pg.K_2, pg.K_3, pg.K_4,
          pg.K_5, pg.K_6, pg.K_7, pg.K_8,
          pg.K_9]
INPUT2 = [pg.K_KP1, pg.K_KP2, pg.K_KP3,
          pg.K_KP4, pg.K_KP5, pg.K_KP6, pg.K_KP7,
          pg.K_KP8, pg.K_KP9]
OUTPUT1 = list(range(49, 58))
OUTPUT2 = list(range(257, 266))

# difficulty
HARD = 70
MEDIUM = 50
EASY = 30
