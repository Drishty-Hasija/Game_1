import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 700
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER = (70, 200, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 40)
screen.fill(BG_COLOR)

board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
player = 'X'
game_over = False
winner = None

def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WIDTH), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                    (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), 
                    CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def check_win(player):
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            draw_vertical_winning_line(col, player)
            return True
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            draw_horizontal_winning_line(row, player)
            return True
    if all(board[i][i] == player for i in range(BOARD_COLS)):
        draw_desc_diagonal(player)
        return True
    if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_COLS)):
        draw_asc_diagonal(player)
        return True
    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE / 2
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, WIDTH - 15), 15)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE / 2
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)

def draw_asc_diagonal(player):
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (15, WIDTH - 15), (WIDTH - 15, 15), 15)

def draw_desc_diagonal(player):
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, WIDTH - 15), 15)

def is_board_full():
    return all(board[row][col] is not None for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def draw_status():
    if winner:
        message = f"{winner} wins!"
    elif is_board_full():
        message = "It's a draw!"
    else:
        message = f"{player}'s turn"
    text = font.render(message, True, TEXT_COLOR)
    screen.fill(BG_COLOR, (0, WIDTH, WIDTH, HEIGHT - WIDTH))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, WIDTH + 20))

def draw_restart_button():
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    text = small_font.render("Restart", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 70))
    return button_rect

def restart():
    global board, player, game_over, winner
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    player = 'X'
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_lines()
    draw_status()

draw_lines()
draw_status()

while True:
    draw_restart_button()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if HEIGHT - 80 < mouseY < HEIGHT - 30:
                restart()
            elif not game_over and mouseY < WIDTH:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        winner = player
                        game_over = True
                    elif is_board_full():
                        game_over = True
                    player = 'O' if player == 'X' else 'X'
                    draw_figures()
                    draw_status()
