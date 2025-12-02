import pygame, sys
from pygame.locals import *

FPS = 60

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 120
paddle_x = 10
paddle_y = (WINDOWHEIGHT - PADDLE_HEIGHT) // 2
PADDLE_SPEED = 7

BALL_SIZE = 15

def reset_ball():
    return WINDOWWIDTH // 2, WINDOWHEIGHT // 2, 4, -4

ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()

def draw():
    DIPSLAYSURF.fill(BLACK)

    pygame.draw.rect(DIPSLAYSURF, GRAY, (0, 0, WINDOWWIDTH, 10))
    pygame.draw.rect(DIPSLAYSURF, GRAY, (0, WINDOWHEIGHT - 10, WINDOWWIDTH, 10))
    pygame.draw.rect(DIPSLAYSURF, GRAY, (WINDOWWIDTH - 10, 0, 10, WINDOWHEIGHT))

    pygame.draw.rect(DIPSLAYSURF, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    pygame.draw.rect(DIPSLAYSURF, RED, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    score_text = BASICFONT.render(f"Score: {score}", True, GREEN)
    DIPSLAYSURF.blit(score_text, (WINDOWWIDTH//2 - 50, 20))

    if paused:
        pause_text = BASICFONT.render("PAUSED - Press P to Resume", True, RED)
        DIPSLAYSURF.blit(pause_text, (WINDOWWIDTH//2 - 60, WINDOWHEIGHT//2 - 20))

    pygame.display.update()


def reset_game():
    global paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y, score
    paddle_y = (WINDOWHEIGHT - PADDLE_HEIGHT) // 2
    ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
    score = 0


def main():
    global DIPSLAYSURF, BASICFONT, score, paused
    global paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y

    pygame.init()
    DIPSLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Pong")
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)

    score = 0
    paused = False

    while True:
        draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_p:
                    paused = not paused

                if event.key == K_r:
                    reset_game()

        if paused:
            continue

        keys = pygame.key.get_pressed()
        if keys[K_UP] and paddle_y > 10:
            paddle_y -= PADDLE_SPEED
        if keys[K_DOWN] and paddle_y < WINDOWHEIGHT - PADDLE_HEIGHT - 10:
            paddle_y += PADDLE_SPEED

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 10 or ball_y + BALL_SIZE >= WINDOWHEIGHT - 10:
            ball_speed_y *= -1

        if ball_x + BALL_SIZE >= WINDOWWIDTH - 10:
            ball_speed_x *= -1


        if ball_x < paddle_x + PADDLE_WIDTH:
            if paddle_y <= ball_y <= paddle_y + PADDLE_HEIGHT:
                ball_speed_x *= -1
                ball_speed_x *= 1.1
                ball_speed_y *= 1.1
                score += 1
            else:
                OVER_text = BASICFONT.render("GAME OVER", True, RED)
                DIPSLAYSURF.blit(OVER_text, (WINDOWWIDTH // 2 - 60, WINDOWHEIGHT // 2 - 20))
                pygame.display.update()
                pygame.time.wait(5000)
                pygame.quit()
                sys.exit()

        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
