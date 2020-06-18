import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

ROW_COUNT = 6
COLUMN_COUNT = 7

score = 0
curr_score = 0


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    for a in range(ROW_COUNT):
        for b in range(COLUMN_COUNT):
            board[a][b] = random.randint(1, 4)
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return True  # board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    for a in board:
        for b in a:
            if b != 0:
                return False
    return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 3:
                pygame.draw.circle(screen, WHITE, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 4:
                pygame.draw.circle(screen, ORANGE, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 5:
                pygame.draw.circle(screen, CYAN, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def check(a1, i, j, tgt, visited):
    visited[i][j] = 1
    a1[i][j] = 0
    global curr_score
    curr_score = curr_score + 1
    if j + 1 < len(a1[0]):
        if a1[i][j + 1] == tgt and visited[i][j + 1] == 0:
            check(a1, i, j + 1, tgt, visited)
    if j - 1 >= 0:
        if a1[i][j - 1] == tgt and visited[i][j - 1] == 0:
            check(a1, i, j - 1, tgt, visited)
    if i - 1 >= 0:
        if a1[i - 1][j] == tgt and visited[i - 1][j] == 0:
            check(a1, i - 1, j, tgt, visited)
    if i + 1 < len(a1):
        if a1[i + 1][j] == tgt and visited[i + 1][j] == 0:
            check(a1, i + 1, j, tgt, visited)


def remove_adjacent(board, row, col):
    visited = np.zeros((ROW_COUNT, COLUMN_COUNT))
    check(board, row, col, board[row][col], visited)


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("retro-computer", 40)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #if event.type == pygame.MOUSEMOTION:
        #    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
        #    posx = event.pos[0]
        #    if turn == 0:
        #        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
        #    else:
        #        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        #pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = ROW_COUNT - int(math.floor(event.pos[1] / SQUARESIZE))  # get_next_open_row(board, col)
                    # drop_piece(board, row, col, 1)
                    remove_adjacent(board, row, col)
                    score = score + 1#1/curr_score + score

                    curr_score = 0
                    if winning_move(board, 1):
                        label = myfont.render("Cleared with " + str(score) + " points", 1, RED)
                        screen.blit(label, (30, 10))
                        game_over = True
                    else:
                        label = myfont.render("Score: " + str(score), 1, RED)
                        screen.blit(label, (20, 5))


            # # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            # turn += 1
            # turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
