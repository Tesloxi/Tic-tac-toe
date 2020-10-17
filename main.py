#!/usr/bin/python3
# -*- coding: utf-8 -*

"""Tic-tac-toe game with pygame."""

import os
import tkinter as tk

from pygame import *
from random import choice
from time import sleep

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
grid = [['E' for _ in range(3)] for _ in range(3)] # Matrix containing the squares and what is inside (either a cross X or a circle O)
#grid = [['X', 'X', 'X'], ['X', 'X', 'X'], ['X', 'X', 'X']]
player = True
turns = 0

def bot(grid):
    """Choose the best place for the bot to play"""
    empty_cases = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'E':
                empty_cases.append((i, j))
    if len(empty_cases) > 1:
        i, j = choice(empty_cases)
        grid[i][j] = 'O'
        sleep(.5)



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
                    x, y, p = s*j, s*i, int(s*.2)
                    draw.polygon(surface, cross_color, [(x+p+r, y+p-r), (x+p-r, y+p+r), (x+s-p-r, y+s-p+r), (x+s-p+r, y+s-p-r)])
                    draw.polygon(surface, cross_color, [(x+s-p-r, y+p-r), (x+p-r, y+s-p-r), (x+p+r, y+s-p+r), (x+s-p+r, y+p+r)])

def won(grid):
    """Check if three same tokens are aligned"""
    for i in range(len(grid)):
        ri = list(set(grid[i])) #rows
        if len(ri) == 1 and ri[0] != 'E':
            print(ri[0] + ' wins !')
            return True
        rj = list(set([grid[j][i] for j in range(len(grid[i]))])) #cols
        if len(rj) == 1 and rj[0] != 'E':
            print(rj[0] + ' wins !')
            return True

    diag_lr = list(set([grid[i][i] for i in range(len(grid))])) # diagonal from top left to bottom right
    if len(diag_lr) == 1 and diag_lr[0] != 'E':
            print(diag_lr[0] + ' wins !')
            return True
            
    diag_rl = list(set([grid[i][len(grid) - i - 1] for i in range(len(grid))])) # diagonal from top right to bottom left
    if len(diag_rl) == 1 and diag_rl[0] != 'E':
            print(diag_rl[0] + ' wins !')
            return True

# Setup game loop
FPS = 60
clock = time.Clock()
run = True

win.fill(BACKGROUND)

while run:
    clock.tick(FPS)

    events = event.get()

    for e in events:
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): run = False

    if player:
        for e in events:
            if player and e.type == MOUSEBUTTONUP and e.button == 1:
                x, y = mouse.get_pos()
                x, y = x - (SIZE - GRID_SIZE) // 2, y - (SIZE - GRID_SIZE) // 2
                x, y = x//100, y//100
                if grid[y][x] == 'E': 
                    grid[y][x] = 'X'
                    player = False
                    turns += 1
    else:
        bot(grid)
        player = True
        turns += 1
           
    draw_grid(grid_surface, LINE, CIRCLE, CROSS, grid)
    win.blit(grid_surface, (GRID_X, GRID_Y))
    display.update()

    if turns == 9:
        run = False
    elif turns >= 5:
        run = not won(grid)

sleep(2)
print(*grid)
quit()