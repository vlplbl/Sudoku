from os import path
import sys
import pygame as pg
from board import Tile, draw_text, draw_button
from settings import *
from generator import generate_board, solve


class Game:
    def __init__(self):
        self.running = True
        self.playing = True
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Sudoku")
        self.difficulty = None
        self.starting = True
        self.clock = pg.time.Clock()
        # so that the one file .exe can get the external font file
        if getattr(sys, 'frozen', False):
            game_folder = sys._MEIPASS
        else:
            game_folder = path.dirname(__file__)
        self.font = path.join(game_folder, "Freesansbold.ttf")

    def new(self):
        self.board = [[Tile(self, j*TILESIZE, i*TILESIZE) for i in range(9)]
                      for j in range(9)]
        self.screen.fill(WHITE)
        draw_text(self.screen, BLACK, self.font, "Generating Board...",
                  WIDTH*1/4, HEIGHT*1/2, 30)
        pg.display.flip()
        self.matrix = generate_board(self.difficulty)
        self.user_matrix = [[self.matrix[col][row] for row in range(
            len(self.matrix))] for col in range(len(self.matrix[0]))]
        for col in self.board:
            for tile in col:
                if self.matrix[tile.pos[1]][tile.pos[0]] == 0:
                    continue
                else:
                    tile.number = self.matrix[tile.pos[1]][tile.pos[0]]
                    tile.generated = True
        
        self.clicked = False
        self.input = ""
        self.previous_tile = None
        self.waiting = True

        # draw the board initially for optimal performance
        self.screen.fill(WHITE)
        for col in self.board:
            for tile in col:
                tile.initial_draw()

        self.run()

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                self.clicked = True
            if event.type == pg.KEYDOWN:
                if event.key in INPUT1:
                    self.input = OUTPUT1.index(event.key) + 1
                if event.key in INPUT2:
                    self.input = OUTPUT2.index(event.key) + 1

    def update(self):
        counter = 0
        for col in self.board:
            for tile in col:
                if tile.number != "":
                    counter += 1
                if counter == len(self.board)*len(self.board[0]):
                    self.check_for_win(tile)
                if tile.pos == self.get_mouse_pos() and self.clicked:
                    tile.selected = True
                    self.input = ""
                    # if the tile is one of the initially shown tiles
                    if tile.generated:
                        tile.selected = False
                    if self.previous_tile and self.previous_tile != tile:
                        self.previous_tile.selected = False
                    self.clicked = False

        for col in self.board:
            for tile in col:
                if tile.selected:
                    self.previous_tile = tile
                    tile.number = str(self.input)
                    self.user_matrix[tile.pos[1]
                                     ][tile.pos[0]] = self.input

    def draw(self):

        def show_solution():
            # function for the solve button
            solve(self.matrix)
            for col in self.board:
                for tile in col:
                    tile.selected = False
                    tile.number = self.matrix[tile.pos[1]][tile.pos[0]]
            self.user_matrix = self.matrix

        # pg.display.set_caption(f"FPS:{self.clock.get_fps():.2g}")

        for col in self.board:
            for tile in col:
                if tile.selected:
                    tile.draw()

        # draw thick line each 3 blocks
        for i in range(3, 8, 3):
            pg.draw.line(self.screen, BLACK,
                         (0, i*TILESIZE), (WIDTH, i*TILESIZE), 5)
            pg.draw.line(self.screen, BLACK,
                         (i*TILESIZE, 0), (i*TILESIZE, HEIGHT - TILESIZE), 5)
        

        draw_button(self.screen, "SOLVE", YELLOW, LIGHTYELLOW,
                    WIDTH*6/8, HEIGHT - 60, 130, 50, self.font, show_solution)
        pg.display.flip()

    def get_mouse_pos(self):
        mx, my = pg.mouse.get_pos()
        return (mx//TILESIZE, my//TILESIZE)

    def check_for_win(self, tile):
        self.copy_matrix = [[self.matrix[col][row] for row in range(
            len(self.matrix))] for col in range(len(self.matrix[0]))]
        solve(self.copy_matrix)
        if self.copy_matrix == self.user_matrix:
            self.playing = False

    def start_screen(self):

        def easy():
            self.difficulty = EASY
            self.starting = False

        def medium():
            self.difficulty = MEDIUM
            self.starting = False

        def hard():
            self.difficulty = HARD
            self.starting = False

        while self.starting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.starting = False
                    self.playing = False
                    pg.quit()
                    sys.exit()

            self.screen.fill(WHITE)
            draw_text(self.screen, BLACK, self.font, "Choose difficulty:",
                      WIDTH * 1/5, HEIGHT * 2/3, 40)
            draw_text(self.screen, BLACK, self.font,
                      "SUDOKU", WIDTH * 1/3, HEIGHT * 1/3, 40)
            draw_button(self.screen, "EASY", GREEN, LIGHTGREEN,
                        WIDTH*1/8, HEIGHT*4/5, 130, 50, self.font, easy)
            draw_button(self.screen, "MEDIUM", YELLOW, LIGHTYELLOW,
                        WIDTH*3/8, HEIGHT*4/5, 130, 50, self.font, medium)
            draw_button(self.screen, "HARD", RED, LIGHTRED,
                        WIDTH*5/8, HEIGHT*4/5, 130, 50, self.font, hard)
            pg.display.flip()

    def end_screen(self):

        def quit():
            pg.quit()
            sys.exit()

        def play():
            self.waiting = False
            self.playing = True
            self.starting = True

        while self.waiting:
            self.clock.tick(FPS)            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    pg.quit()
                    sys.exit()

            self.screen.fill(WHITE)
            # play again and quit buttons:
            draw_button(self.screen, "PLAY", GREEN, LIGHTGREEN,
                        WIDTH*2/8, HEIGHT-60, 130, 50, self.font, play)
            draw_button(self.screen, "QUIT", RED, LIGHTRED,
                        WIDTH*4/8, HEIGHT-60, 130, 50, self.font, quit)
            for col in self.board:
                for tile in col:
                    tile.draw()
            for i in range(3, 8, 3):
                pg.draw.line(self.screen, BLACK,
                             (0, i*TILESIZE), (WIDTH, i*TILESIZE), 5)
                pg.draw.line(self.screen, BLACK,
                             (i*TILESIZE, 0), (i*TILESIZE, HEIGHT - TILESIZE), 5)
            pg.display.flip()


if __name__ == "__main__":

    g = Game()
    while g.running:
        g.start_screen()
        g.new()
        g.end_screen()

    pg.quit()
    sys.exit()
