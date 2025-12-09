import pygame, random, sys
from pygame.locals import *

# --------------------
# CONSTANTS
# --------------------
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

BASKETWIDTH = 100
BASKETHEIGHT = 20
BASKETSPEED = 8

APPLE_SIZE = 20
BOMB_SIZE = 20
FALL_SPEED = 5
NEW_OBJECT_INTERVAL = 30

# --------------------
# SETUP
# --------------------
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Catcher Game')
BASICFONT = pygame.font.Font('freesansbold.ttf', 24)
FPSCLOCK = pygame.time.Clock()

# --------------------
# FUNCTIONS
# --------------------
def terminate():
    pygame.quit()
    sys.exit()

def waitForKeyPress():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_RETURN:
                    return

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# --------------------
# MAIN GAME
# --------------------
def main():
    global FALL_SPEED

    basket = pygame.Rect(WINDOWWIDTH // 2 - BASKETWIDTH // 2,
                         WINDOWHEIGHT - 60, BASKETWIDTH, BASKETHEIGHT)
    apples = []
    bombs = []
    moveLeft = moveRight = False
    livesLeft = 3
    lostApples = 0
    score = 0
    frameCount = 0
    warningTimer = 0
    FALL_SPEED = 5  # reset speed each game

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveRight = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False

        # Move basket
        if moveLeft and basket.left > 0:
            basket.left -= BASKETSPEED
        if moveRight and basket.right < WINDOWWIDTH:
            basket.left += BASKETSPEED

        # Spawn apples/bombs
        # every 30 frames (NEW_OBJECT_INTERVAL), spawn a new object (apple or bomb).
        frameCount += 1
        if frameCount % NEW_OBJECT_INTERVAL == 0:
            if random.randint(0, 1) == 0:
                apples.append(pygame.Rect(random.randint(0, WINDOWWIDTH - APPLE_SIZE), 0, APPLE_SIZE, APPLE_SIZE))
            else:
                bombs.append(pygame.Rect(random.randint(0, WINDOWWIDTH - BOMB_SIZE), 0, BOMB_SIZE, BOMB_SIZE))

        # Move apples
        for a in apples[:]:
            a.top += FALL_SPEED
            if a.top > WINDOWHEIGHT:
                apples.remove(a)
                lostApples += 1
            elif a.colliderect(basket):
                apples.remove(a)
                score += 1
                if score % 7 == 0:
                    FALL_SPEED += 1

        # Move bombs
        for b in bombs[:]:
            b.top += FALL_SPEED
            if b.top > WINDOWHEIGHT:
                bombs.remove(b)
            elif b.colliderect(basket):
                bombs.remove(b)
                livesLeft -= 1
                warningTimer = 30

        # --------------------------
        # GAME OVER CONDITION
        # --------------------------
        if lostApples >= 10 or livesLeft <= 0:
            DISPLAYSURF.fill(WHITE)
            drawText("GAME OVER!", BASICFONT, DISPLAYSURF, WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2 - 20, RED)
            drawText(f"Final Score: {score}", BASICFONT, DISPLAYSURF, WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2 + 20, BLACK)
            pygame.display.update()
            pygame.time.wait(2000)
            return

        # Drawing
        DISPLAYSURF.fill(WHITE)
        pygame.draw.rect(DISPLAYSURF, RED, basket)
        for a in apples:
            pygame.draw.rect(DISPLAYSURF, GREEN, a)
        for b in bombs:
            pygame.draw.rect(DISPLAYSURF, BLACK, b)

        drawText(f"Score: {score}", BASICFONT, DISPLAYSURF, 10, 10, BLACK)
        drawText(f"Lives left: {livesLeft}", BASICFONT, DISPLAYSURF, 10, 30, BLACK)
        drawText(f"Missed apples: {lostApples}/10", BASICFONT, DISPLAYSURF, 10, 50, BLACK)

        if warningTimer > 0:
            drawText("WARNING! YOU GOT A BOMB", BASICFONT, DISPLAYSURF, 50, 80, RED)
            warningTimer -= 1

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# --------------------
# MAIN LOOP
# --------------------
while True:
    DISPLAYSURF.fill(WHITE)
    drawText('CATCHER GAME', BASICFONT, DISPLAYSURF, WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2 - 60, RED)
    drawText('Catch green apples, avoid black bombs!', BASICFONT, DISPLAYSURF, WINDOWWIDTH // 2 - 160, WINDOWHEIGHT // 2 - 20, BLACK)
    drawText('Press ENTER to start or ESC to quit.', BASICFONT, DISPLAYSURF, WINDOWWIDTH // 2 - 140, WINDOWHEIGHT // 2 + 20, BLACK)
    pygame.display.update()
    waitForKeyPress()
    main()
