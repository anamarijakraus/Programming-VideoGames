import random, pygame, sys
from pygame.locals import *

pygame.init()

# ---------------- CONFIG ----------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FPS = 30

BOARD_WIDTH = 8
BOARD_HEIGHT = 8
CELL_SIZE = 40

X_MARGIN = (WINDOW_WIDTH - BOARD_WIDTH * CELL_SIZE) // 2
Y_MARGIN = (WINDOW_HEIGHT - BOARD_HEIGHT * CELL_SIZE) // 2

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Candy Crush")
FONT = pygame.font.SysFont(None, 30)

# ---------------- CANDIES ----------------
RED = "red"
BLUE = "blue"
GREEN = "green"
YELLOW = "yellow"
ALL_CANDIES = [RED, BLUE, GREEN, YELLOW]
EMPTY = None

# --------------------------------
CANDY_IMAGES = {
    RED: pygame.transform.scale(pygame.image.load("red.png"), (CELL_SIZE, CELL_SIZE)),
    BLUE: pygame.transform.scale(pygame.image.load("blue.png"), (CELL_SIZE, CELL_SIZE)),
    GREEN: pygame.transform.scale(pygame.image.load("green.png"), (CELL_SIZE, CELL_SIZE)),
    YELLOW: pygame.transform.scale(pygame.image.load("yellow.png"), (CELL_SIZE, CELL_SIZE))
}

# --------------------------------
def getLeftTopOfBox(boxx, boxy):
    left = X_MARGIN + (boxx * CELL_SIZE)
    top = Y_MARGIN + (boxy * CELL_SIZE)
    return left, top

def getBoxAtPixel(mousex, mousey):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)
            if boxRect.collidepoint(mousex, mousey):
                return boxx, boxy
    return None, None

def makeText(text, color, x, y):
    surf = FONT.render(text, True, color)
    rect = surf.get_rect(topleft=(x, y))
    return surf, rect

# --------------------------------
def generateBoard():
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            while True:
                candy = random.choice(ALL_CANDIES)
                horizontal_match = False
                if x >= 2:
                    if board[x - 1][y] == candy and board[x - 2][y] == candy:
                        horizontal_match = True

                vertical_match = False
                if y >= 2:
                    if column[y - 1] == candy and column[y - 2] == candy:
                        vertical_match = True

                if not horizontal_match and not vertical_match:
                    column.append(candy)
                    break

        board.append(column)
    return board

def drawBoard(board, selected):
    screen.fill((100, 100, 100))
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            left, top = getLeftTopOfBox(x, y)
            pygame.draw.rect(screen, (255, 255, 255),
                             (left, top, CELL_SIZE, CELL_SIZE), 1)
            if board[x][y] is not EMPTY:
                screen.blit(CANDY_IMAGES[board[x][y]], (left, top))
            if selected == (x, y):
                pygame.draw.rect(screen, (255, 255, 0),
                                 (left - 3, top - 3, CELL_SIZE + 6, CELL_SIZE + 6), 3)

# --------------------------------
def checkBoardForMatches(board):
    matches = []

    # Vertical
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT - 2):
            candy = board[x][y]
            if candy is not None and candy == board[x][y+1] == board[x][y+2]:
                i = y
                while i < BOARD_HEIGHT and board[x][i] == candy:
                    if (x, i) not in matches:
                        matches.append((x, i))
                    i += 1

    # Horizontal
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH - 2):
            candy = board[x][y]
            if candy is not None and candy == board[x+1][y] == board[x+2][y]:
                i = x
                while i < BOARD_WIDTH and board[i][y] == candy:
                    if (i, y) not in matches:
                        matches.append((i, y))
                    i += 1
    # for x in range(BOARD_WIDTH - 2):
    #     for y in range(BOARD_HEIGHT - 2):
    #         if board[x][y] != None:
    #             candy = board[x][y]
    #             if candy == board[x + 1][y + 1] == board[x + 2][y + 2]:
    #                 i = 0
    #                 while (
    #                         x + i < BOARD_WIDTH and
    #                         y + i < BOARD_HEIGHT and
    #                         board[x + i][y + i] == candy
    #                 ):
    #                     matches.append((x + i, y + i))
    #                     i += 1
    #
    # for x in range(BOARD_WIDTH - 2):
    #     for y in range(2, BOARD_HEIGHT):
    #         if board[x][y] != None:
    #             candy = board[x][y]
    #             if candy == board[x + 1][y - 1] == board[x + 2][y - 2]:
    #                 i = 0
    #                 while (
    #                         x + i < BOARD_WIDTH and
    #                         y - i >= 0 and
    #                         board[x + i][y - i] == candy
    #                 ):
    #                     matches.append((x + i, y - i))
    #                     i += 1
    return matches

def removeMatches(board, matches):
    for x, y in matches:
        board[x][y] = EMPTY

def slideDownCandy(board):
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            if board[x][y] is not EMPTY:
                column.append(board[x][y])

        for y in range(BOARD_HEIGHT - 1, -1, -1):
            if column:
                board[x][y] = column.pop()
            else:
                board[x][y] = random.choice(ALL_CANDIES)

# -------------------------------
def main():
    clock = pygame.time.Clock()
    board = generateBoard()
    firstSelection = None
    score = 0

    while True:
        mouseClicked = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mx, my)

        if mouseClicked and boxx is not None:
            if firstSelection is None:
                firstSelection = (boxx, boxy)
            else:
                x1, y1 = firstSelection
                x2, y2 = boxx, boxy
                if abs(x1 - x2) + abs(y1 - y2) == 1:
                    board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]
                    if not checkBoardForMatches(board):
                        board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]
                firstSelection = None

        matches = checkBoardForMatches(board)
        if matches:
            score += 10
            removeMatches(board, matches)
            slideDownCandy(board)

        drawBoard(board, firstSelection)
        scoreSurf, scoreRect = makeText(f"Score: {score}", (255,255,255), 20, 20)
        screen.blit(scoreSurf, scoreRect)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
