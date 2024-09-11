import sys
import pygame
import numpy as np 

pygame.init()

# Proportions 
width = 300
height = 300
line_width = 5
Board_rows = 3
Board_cols = 3
sq_size = width // Board_cols
circle_rd = sq_size // 3
circle_wd = 15
cross_wd = 25

# Colors
black = (64, 64, 64)
grey = (224, 224, 224)
green = (0, 153, 0)
red = (204, 0, 0)
white = (204, 229, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(black)

board = np.zeros((Board_rows, Board_cols))  

def draw_lines(color=white):
    for i in range(1, Board_rows):
        pygame.draw.line(screen, color, (0, sq_size * i), (width, sq_size * i), line_width)
        pygame.draw.line(screen, color, (sq_size * i, 0), (sq_size * i, height), line_width)

def draw_figures(color=white):
    for row in range(Board_rows):
        for col in range(Board_cols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * sq_size + sq_size // 2), int(row * sq_size + sq_size // 2)), circle_rd, circle_wd)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col * sq_size + sq_size // 4, row * sq_size + sq_size // 4), (col * sq_size + 3 * sq_size // 4, row * sq_size + 3 * sq_size // 4), cross_wd)
                pygame.draw.line(screen, color, (col * sq_size + sq_size // 4, row * sq_size + 3 * sq_size // 4), (col * sq_size + 3 * sq_size // 4, row * sq_size + sq_size // 4), cross_wd)

def mark_square(row, col, player):
    board[row][col] = player

def available_sq(row, col):
    return board[row][col] == 0

def is_full(check_board=board):
    for row in range(Board_rows):
        for col in range(Board_cols):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    # Check columns
    for col in range(Board_cols):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    
    # Check rows
    for row in range(Board_rows):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    
    # Check diagonals
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_full(minimax_board):
        return 0
    
    if is_maximizing:
        best_score = -1000
        for row in range(Board_rows):
            for col in range(Board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(Board_rows):
            for col in range(Board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(Board_rows):
        for col in range(Board_cols):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart_game():
    screen.fill(black)
    draw_lines()
    for row in range(Board_rows):
        for col in range(Board_cols):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // sq_size
            mouseY = event.pos[1] // sq_size

            if available_sq(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1

                if not game_over:
                    if is_full():
                        game_over = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(green)
            draw_lines(green)
        elif check_win(2):
            draw_figures(red)
            draw_lines(red)
        else:
            draw_figures(grey)
            draw_lines(grey)
    
    pygame.display.update() 
