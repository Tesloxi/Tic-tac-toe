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
display.set_icon(image.load("icon.png"))

GRID_SIZE = 300

GRID_X = SIZE // 2 - GRID_SIZE // 2
GRID_Y = SIZE // 2 - GRID_SIZE // 2

grid_surface = Surface((GRID_SIZE, GRID_SIZE), SRCALPHA) # window containing only the grid

# Colors 
BACKGROUND = (20, 189, 172)
CIRCLE = (242, 235, 211)
CROSS = (84, 84, 84)
LINE = (13, 161, 146)
WHITE = (255, 255, 255)

# Fonts
MODES = font.SysFont('calibri', 25)
END = font.SysFont('calibri', 40)

# Games settings
grid = [['E' for _ in range(3)] for _ in range(3)] # Matrix containing the squares and what is inside (either a cross X or a circle O)
player = True
turns = 0
mode = 'medium'

def bot(grid, mode):
    """Choose the best place for the bot to play"""
    empty_cases = []
    o, a = 0, 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'E':
                empty_cases.append((i, j))

    if mode == 'easy':
        o, a = choice(empty_cases)
    elif mode == 'medium':
        o, a = choice(empty_cases)
        if turns >= 3:
            # Check diagonal from top left to bottom right
            dlr = [grid[i][i] for i in range(len(grid))]        
            sdlr = list(set(dlr))  
            if len(sdlr) == 2 and dlr.count('E') == 1:
                o, a = dlr.index('E'), dlr.index('E')

            # Check diagonal from top right to bottom left
            drl = [grid[i][len(grid) - i - 1] for i in range(len(grid))]        
            sdrl = list(set(drl))  
            if len(sdrl) == 2 and drl.count('E') == 1:
                o, a = drl.index('E'), len(drl) - 1 - drl.index('E')

            for i in range(len(grid)):
                # Check rows 
                ri = grid[i]
                sri = list(set(ri))
                if len(sri) == 2 and ri.count('E') == 1:
                    if 'O' in sri:
                        o, a = i, ri.index('E')
                        break
                    elif 'X' in sri:
                        o, a = i, ri.index('E')

                # Check cols
                rj = [grid[j][i] for j in range(len(ri))]
                srj = list(set(rj))
                if len(srj) == 2 and rj.count('E') == 1:
                    if 'O' in srj:
                        o, a = rj.index('E'), i
                        break
                    elif 'X' in srj:
                        o, a = rj.index('E'), i
            
    grid[o][a] = 'O'
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
                    draw.circle(surface, circle_color, (s//2+j*100, s//2+i*100), s*30//100, 6)
                elif grid[i][j] == 'X':
                    # Draw cross
                    r = 2
                    x, y, p = s*j, s*i, s*20//100
                    print(x, y, p)
                    draw.polygon(surface, cross_color, [(x+p+r, y+p-r), (x+p-r, y+p+r), (x+s-p-r, y+s-p+r), (x+s-p+r, y+s-p-r)])
                    draw.polygon(surface, cross_color, [(x+s-p-r, y+p-r), (x+p-r, y+s-p-r), (x+p+r, y+s-p+r), (x+s-p+r, y+p+r)])

def draw_mode_buttons(surface, background,  color, mode):
    """Draw the buttons changing the game mode"""
    w = 100
    h = w * 40 // 100
    l1 = SIZE//2 - w - w*20//100
    l2 =  SIZE//2 + w*20//100
    t = (SIZE - GRID_SIZE)//4 - h//2

    if mode == 'easy':
        draw.line(surface, color, (l1, t + h), (l1 + w, t + h))
        draw.line(surface, background, (l2, t + h), (l2 + w, t + h))
    elif mode == 'medium':
        draw.line(surface, background, (l1, t + h), (l1 + w, t + h))
        draw.line(surface, color, (l2, t + h), (l2 + w, t + h))

    text = MODES.render('EASY', 1, color)
    surface.blit(text, (l1 + w//2 - text.get_width()//2, t + h//2 - text.get_height()//2))
    text = MODES.render('MEDIUM', 1, color)
    surface.blit(text, (l2 + w//2 - text.get_width()//2, t + h//2 - text.get_height()//2))

def draw_won_line(surface, won, circle_color, cross_color):
    """Draw a line on the three wining squares"""
    if not won: won = ([], 1, 'draw')
    winner, n, t = won
    color = circle_color
    if winner == 'X': color = cross_color
    s = surface.get_width()

    if t == 'row':
        draw.line(surface, color, (0, s//6 + s//3*n), (s, s//6 + s//3*n), 6)
    elif t == 'col':
        draw.line(surface, color, (s//6 + s//3*n, 0), (s//6 + s//3*n, s), 6)
    elif t == 'dlr':
        draw.polygon(surface, color, [(4, 0), (0, 4), (s-4, s), (s, s-4)])
    elif t == 'drl':
        draw.polygon(surface, color, [(s-4, 0), (s, 4), (4, s), (0, s-4)])


def won(grid):
    """Check if three same tokens are aligned"""
    for i in range(len(grid)):
        ri = list(set(grid[i])) #rows
        if len(ri) == 1 and ri[0] != 'E':
            return (ri[0], i, 'row')
        rj = list(set([grid[j][i] for j in range(len(grid[i]))])) #cols
        if len(rj) == 1 and rj[0] != 'E':
            return (rj[0], i, 'col')

    diag_lr = list(set([grid[i][i] for i in range(len(grid))])) # diagonal from top left to bottom right
    if len(diag_lr) == 1 and diag_lr[0] != 'E':
            return (diag_lr[0], 1, 'dlr')
            
    diag_rl = list(set([grid[i][len(grid) - i - 1] for i in range(len(grid))])) # diagonal from top right to bottom left
    if len(diag_rl) == 1 and diag_rl[0] != 'E':
            return (diag_rl[0], 1,  'drl')

    return False

# Setup game loop
FPS = 30
clock = time.Clock()
run = True
play = True

# End screen
end = True
w = 200
h = w // 4
l = SIZE//2 - w//2 
t1 = SIZE//2 - h - h//4
t2 = SIZE//2 + h//4

win.fill(BACKGROUND)
draw_mode_buttons(win, BACKGROUND, WHITE, mode)

while run:
    clock.tick(FPS)

    while play:
        events = event.get()

        for e in events:
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): 
                play = False
                end = False
                run = False

        if player:
            for e in events:
                if player and e.type == MOUSEBUTTONUP and e.button == 1:
                    x, y = mouse.get_pos()
                    if x >= GRID_X and x <= GRID_X + GRID_SIZE and\
                    y >= GRID_Y and y <= GRID_Y + GRID_SIZE:
                        x, y = x - (SIZE - GRID_SIZE) // 2, y - (SIZE - GRID_SIZE) // 2
                        x, y = x//100, y//100
                        if grid[y][x] == 'E': 
                            grid[y][x] = 'X'
                            player = False
                            turns += 1
                    elif y >= 30 and y <= 70:
                        if x >= 140 and x <= 240:
                            mode = 'easy'
                        elif x >= 260 and x <= 360:
                            mode = 'medium'
                        draw_mode_buttons(win, BACKGROUND, WHITE, mode)
        else:
            bot(grid, mode)
            player = True
            turns += 1
        
        draw_grid(grid_surface, LINE, CIRCLE, CROSS, grid)
        win.blit(grid_surface, (GRID_X, GRID_Y))
        display.update()

        if turns == 9:
            play = False
            end = not play
        elif turns >= 5:
            play = not won(grid)
            end = not play


    if end:
        sleep(.5)
        draw_won_line(grid_surface, won(grid), CIRCLE, CROSS)
        win.blit(grid_surface, (GRID_X, GRID_Y))
        display.update()
        sleep(1)
        draw.rect(win, BACKGROUND, (l, t1, w, h))
        draw.rect(win, BACKGROUND, (l, t2, w, h))
        draw.rect(win, LINE, (l, t1, w, h), 4)
        draw.rect(win, LINE, (l, t2, w, h), 4)

        text = END.render('REPLAY', 1, CIRCLE)
        win.blit(text, (l + w//2 - text.get_width()//2, t1 + h//2 - text.get_height()//2))
        text = END.render('QUIT', 1, CROSS)
        win.blit(text, (l + w//2 - text.get_width()//2, t2 + h//2 - text.get_height()//2))
        display.update()
        end = False

    events = event.get()

    for e in events:
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): 
            run = False
        elif e.type == MOUSEBUTTONUP and e.button == 1:
            x, y = mouse.get_pos()
            if x >= l and x <= l + w:
                if y >= t1 and y <= t1 + h:
                    win.fill(BACKGROUND)
                    draw_mode_buttons(win, BACKGROUND, WHITE, mode)
                    grid_surface.fill((0, 0, 0, 0))
                    grid = [['E' for _ in range(3)] for _ in range(3)]
                    player = True
                    turns = 0
                    play = True
                elif y >= t2 and y <= t2 + h:
                    run = False

quit()