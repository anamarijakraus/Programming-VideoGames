import pygame, sys, time
from pygame.locals import *

pygame.init()

# ==============================
# LEVEL MATRIX
# 0 = empty
# 1 = wall
# 2 = start
# 3 = end
# 4 = trap
# ==============================

LEVEL = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,2,0,0,4,0,0,0,0,1],
    [1,0,1,0,1,0,1,4,0,1],
    [1,0,1,0,0,0,1,0,0,1],
    [1,0,4,0,1,0,0,0,4,1],
    [1,0,1,0,1,0,1,0,0,1],
    [1,0,0,0,0,4,0,0,0,1],
    [1,0,1,1,1,0,1,1,0,1],
    [1,0,0,4,0,0,0,3,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

GRID_ROWS = len(LEVEL)
GRID_COLS = len(LEVEL[0])

# ==============================
# WINDOW + COLORS
# ==============================

TILE = 40
MARGIN = 40
STATUS_BAR_H = 40

WINDOW_WIDTH = GRID_COLS * TILE + MARGIN * 2
WINDOW_HEIGHT = GRID_ROWS * TILE + MARGIN * 2 + STATUS_BAR_H

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Trap Maze")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
BLUE = (0,0,200)
GREEN = (0,200,0)
GRAY = (200,200,200)
ORANGE = (250,150,0)

font = pygame.font.SysFont(None, 28)

# ==============================
# EXTRACT START, TRAPS, END  (x, y)
# ==============================

start_pos = None
end_pos = None
traps = []

for y in range(GRID_ROWS):
    for x in range(GRID_COLS):
        if LEVEL[y][x] == 2:
            start_pos = (x, y)
        elif LEVEL[y][x] == 3:
            end_pos = (x, y)
        elif LEVEL[y][x] == 4:
            traps.append((x, y))

# ==============================
# GAME STATE
# ==============================

player = start_pos
game_state = "REVEAL"
reveal_time = pygame.time.get_ticks()
lives = 3
moves = 0
message = ""

# ==============================
# STATUS MESSAGE
# ==============================

def set_message(msg):
    global message
    message = msg

# ==============================
# VALID MOVE (x, y)
# ==============================

def isValidMove(player, move):
    x, y = player

    if move == "UP" and y - 1 < 0:
        return False
    elif move == "DOWN" and y + 1 > GRID_ROWS - 1:
        return False
    elif move == "LEFT" and x - 1 < 0:
        return False
    elif move == "RIGHT" and x + 1 > GRID_COLS - 1:
        return False
    return True

# ==============================
# DRAW GRID + PLAYER + STATUS BAR
# ==============================

def draw():
    screen.fill(WHITE)

    # Status bar
    pygame.draw.rect(screen, GRAY, (0,0,WINDOW_WIDTH,STATUS_BAR_H))
    text = font.render(f"Lives: {lives}   Moves: {moves}   {message}", True, BLACK)
    screen.blit(text, (10, 10))

    # Maze grid
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            cell = LEVEL[y][x]

            sx = MARGIN + x * TILE
            sy = MARGIN + y * TILE + STATUS_BAR_H

            color = WHITE
            if cell == 1:
                color = BLACK
            elif cell == 3:
                color = GREEN

            pygame.draw.rect(screen, color, (sx, sy, TILE, TILE))

            # traps revealed only in REVEAL state
            if game_state == "REVEAL" and cell == 4:
                pygame.draw.rect(screen, ORANGE, (sx, sy, TILE, TILE))

    # draw player
    px, py = player
    pxs = MARGIN + px*TILE + TILE//2
    pys = MARGIN + py*TILE + TILE//2 + STATUS_BAR_H
    pygame.draw.circle(screen, BLUE, (pxs, pys), TILE//3)

    pygame.display.flip()

# ==============================
# MAIN LOOP
# ==============================

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Escape exits game
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

        # Restart
        if event.type == KEYDOWN and event.key == K_r:
            player = start_pos
            lives = 3
            moves = 0
            message = ""
            game_state = "REVEAL"
            reveal_time = pygame.time.get_ticks()

        # PLAY STATE MOVEMENT
        if game_state == "PLAY":
            if event.type == KEYDOWN:

                direction = None
                if event.key == K_LEFT:
                    direction = "LEFT"
                elif event.key == K_RIGHT:
                    direction = "RIGHT"
                elif event.key == K_UP:
                    direction = "UP"
                elif event.key == K_DOWN:
                    direction = "DOWN"

                if direction:
                    x, y = player
                    new_player = player

                    # ======================
                    # Your required style
                    # ======================
                    if direction == "UP" and isValidMove(player, direction):
                        new_player = (x, y - 1)
                    elif direction == "DOWN" and isValidMove(player, direction):
                        new_player = (x, y + 1)
                    elif direction == "LEFT" and isValidMove(player, direction):
                        new_player = (x - 1, y)
                    elif direction == "RIGHT" and isValidMove(player, direction):
                        new_player = (x + 1, y)

                    # No movement → invalid
                    if new_player == player:
                        set_message("Invalid move!")
                    else:
                        nx, ny = new_player

                        # WALL
                        if LEVEL[ny][nx] == 1:
                            lives -= 1
                            set_message("Hit a wall! -1 life")
                            player = start_pos

                        # TRAP
                        elif (nx, ny) in traps:
                            lives -= 1
                            set_message("Stepped on a trap! -1 life")
                            player = start_pos

                        else:
                            # VALID MOVE
                            moves += 1
                            player = new_player
                            set_message("")

                            # WIN
                            if (nx, ny) == end_pos:
                                set_message("You reached the end! YOU WIN!")
                                game_state = "WIN"

                        # LOSE
                        if lives <= 0:
                            set_message("No lives left! GAME OVER!")
                            game_state = "LOSE"

    # Reveal state timeout
    if game_state == "REVEAL":
        if pygame.time.get_ticks() - reveal_time > 4000:
            game_state = "PLAY"

    draw()
