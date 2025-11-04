import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 500
WINDOWHEIGHT = 600
BOXSIZE = 80
GAPSIZE = 10
COLORBOXSIZE = 60

BOARDWIDTH = 5
BOARDHEIGHT = 5

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210,210,210)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BGCOLOR = GRAY
BOXCOLOR = WHITE
COLORS = [RED, GREEN, BLUE, YELLOW]


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def generateEmptyBoard():
    return [[None] * BOARDHEIGHT for _ in range(BOARDWIDTH)]

def drawBoard(board):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            color = board[boxx][boxy] if board[boxx][boxy] else BOXCOLOR
            pygame.draw.rect(DISPLAYSURF, color, (left, top, BOXSIZE, BOXSIZE))


def generateColorMenuBoard():
    return [[color] for color in COLORS]


def drawColorMenuBoard(colorMenuBoard):
    global menuY
    gap = 20
    menuY = YMARGIN + BOARDHEIGHT * (BOXSIZE + GAPSIZE) + 20

    for i, colorColumn in enumerate(colorMenuBoard):
        color = colorColumn[0]
        left = XMARGIN + i * (COLORBOXSIZE + gap)
        pygame.draw.rect(DISPLAYSURF, color, (left, menuY, COLORBOXSIZE, COLORBOXSIZE))
        if color == selectedColor:
            pygame.draw.rect(DISPLAYSURF, WHITE, (left - 2, menuY - 2, COLORBOXSIZE + 4, COLORBOXSIZE + 4), 3)

def getColorBoxAtPixel(mousex, mousey, colorMenuBoard):
    gap = 20
    for i, colorColumn in enumerate(colorMenuBoard):
        left = XMARGIN + i * (COLORBOXSIZE + gap)
        colorRect = pygame.Rect(left, menuY, COLORBOXSIZE, COLORBOXSIZE)
        if colorRect.collidepoint(mousex, mousey):
            return i
    return None


def handleColorMenuClick(mousex, mousey, colorMenuBoard):
    global selectedColor
    i = getColorBoxAtPixel(mousex, mousey, colorMenuBoard)
    if i is not None:
        selectedColor = colorMenuBoard[i][0]


def isValidMove(board, boxx, boxy, color):
    neighbors = getNeighbors(boxx, boxy)
    for neighbor in neighbors:
        if board[neighbor[0]][neighbor[1]] == color:
            return False
    return True


def getNeighbors(boxx, boxy):
    neighbors = []
    if boxx > 0:
        neighbors.append((boxx - 1, boxy))
    if boxx < BOARDWIDTH - 1:
        neighbors.append((boxx + 1, boxy))
    if boxy > 0:
        neighbors.append((boxx, boxy - 1))
    if boxy < BOARDHEIGHT - 1:
        neighbors.append((boxx, boxy + 1))
    return neighbors


def isBoardComplete(board):
    for row in board:
        if None in row:
            return False
    return True


def showWinMessage():
    font = pygame.font.Font(None, 72)
    text = font.render('You win!', True, WHITE, GREEN)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(text, textRect)
    pygame.display.update()


def drawMessage(message):
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, WHITE, RED)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(text, textRect)
    pygame.display.update()


def showInstructions():
    fontTitle = pygame.font.Font(None, 64)
    fontText = pygame.font.Font(None, 30)

    title = fontTitle.render("Welcome!", True, GREEN)
    titleRect = title.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 6))

    instructions = [
        "Instructions:",
        "- Choose a color from the menu below the board.",
        "- Click on an empty field to color it.",
        "- Adjacent fields must not be the same color!",
        "- The goal is to color all the fields."
    ]
    instructionRects = []
    for i, line in enumerate(instructions):
        text = fontText.render(line, True, BLACK)
        rect = text.get_rect(center=(WINDOWWIDTH / 2, WINDOWHEIGHT / 3 + i * 30))
        instructionRects.append((text, rect))

    start = fontTitle.render("Click to start.", True, RED)
    startRect = start.get_rect(center=(WINDOWWIDTH / 2, 450))

    while True:
        DISPLAYSURF.fill(GRAY)

        DISPLAYSURF.blit(title, titleRect)
        for text, rect in instructionRects:
            DISPLAYSURF.blit(text, rect)
        DISPLAYSURF.blit(start, startRect)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return

        pygame.display.update()


def main():
    global FPSCLOCK, DISPLAYSURF, selectedColor
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Color Fill Game')

    showInstructions()

    board = generateEmptyBoard()
    colorMenuBoard = generateColorMenuBoard()

    selectedColor = COLORS[0]
    livesLeft = 3

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        font = pygame.font.Font(None, 36)
        livesLeftText = font.render(f"Lives left: {livesLeft}", True, RED)
        DISPLAYSURF.blit(livesLeftText, (XMARGIN, YMARGIN - 40))
        drawBoard(board)
        drawColorMenuBoard(colorMenuBoard)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if mousey > YMARGIN + BOARDHEIGHT * (BOXSIZE + GAPSIZE):
                    handleColorMenuClick(mousex, mousey, colorMenuBoard)
                else:
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
                    if board[boxx][boxy] is None:
                        if isValidMove(board, boxx, boxy, selectedColor):
                            board[boxx][boxy] = selectedColor
                            if isBoardComplete(board):
                                drawBoard(board)
                                showWinMessage()
                                pygame.time.wait(5000)
                                pygame.quit()
                                sys.exit()
                        else:
                            livesLeft -= 1

                            if livesLeft == 0:
                                drawMessage("You lose!")
                                pygame.time.wait(3000)
                                pygame.quit()
                                sys.exit()
                            else:
                                drawMessage("Invalid move!")
                                pygame.time.wait(1500)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
