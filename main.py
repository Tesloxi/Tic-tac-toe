#!/usr/bin/python3
# -*- coding: utf-8 -*

"""Tic-tac-toe game with pygame."""

import os
import tkinter as tk

from pygame import *

init()

# Setup display

root = tk.Tk()

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

SIZE = 500

win_x = screen_width // 2 - SIZE // 2
win_y = screen_height // 2 - SIZE // 2

os.environ["SDL_VIDEO_WINDOW_POS"] = str(win_x) + ',' + str(win_y)
win = display.set_mode((SIZE, SIZE)) # main window
display.set_caption("Tic-tac-toe")

GRID_SIZE = 300

GRID_X = SIZE // 2 - GRID_SIZE // 2
GRID_Y = SIZE // 2 - GRID_SIZE // 2

grid_surface = Surface((GRID_SIZE, GRID_SIZE), SRCALPHA) # window containing only the grid

# Colors 
BACKGROUND = (20, 189, 172)
CIRCLE = (242, 235, 211)
CROSS = (84, 84, 84)
LINE = (13, 161, 146)

# Games settings
#grid = [['E' for _ in range(3)] for _ in range(3)] # Matrix containing the squares and what is inside (either a cross X or a circle O)
grid = [['X', 'X', 'X'],['X', 'O', 'X'],['X', 'X', 'X']]

def draw_grid(surface, color, circle_color, cross_color, grid):
    """Draw the grid and the circles or crosses in it"""
    s = surface.get_width()
    for i in range(1, 3): # vertical lines
        draw.line(surface, color, (0, s*i//3), (s, s*i//3), 6)
        draw.line(surface, color, (s*i//3, 0), (s*i//3, s), 6)
        
    s //= 3

    for i in range(len(grid)):
        if 'O' in grid[i] or 'X' in grid[i]:
            for j in range(len(grid[i])):
                if grid[i][j] == 'O':
                    # Draw circle
                    draw.circle(surface, circle_color, (s//2+j*100, s//2+i*100), int(s*.3), 6)
                elif grid[i][j] == 'X':
                    # Draw cross
                    r = 2
                    draw.polygon(surface, cross_color, [(int(s*.2+r), int(s*.2-r)), (int(s*.2-r), int(s*.2+r)), (int(s-s*.2-r), int(s-s*.2+r)), (int(s-s*.2+r), int(s-s*.2-r))])
                    draw.polygon(surface, cross_color, [(int(s*.2-r), int(s-s*.2-r)), (int(s*.2+r), int(s-s*.2+r)), (int(s-s*.2+r), int(s*.2+r)), (int(s-s*.2-r), int(s*.2-r))])

# Setup game loop
FPS = 60
clock = time.Clock()
run = True

win.fill(BACKGROUND)
draw_grid(grid_surface, LINE, CIRCLE, CROSS, grid)
win.blit(grid_surface, (GRID_X, GRID_Y))
display.update()

while run:
    clock.tick(FPS)

    for e in event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): run = False

quit()