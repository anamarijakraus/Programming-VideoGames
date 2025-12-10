import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

background_music = "background_music.wav"
clash_sound = pygame.mixer.Sound("clash_sound.wav")
asteroid_img = pygame.image.load("asteroid.png")
spaceship_img = pygame.image.load("spaceship.png")
crystal_img = pygame.image.load("energy_crystal.png")
bg = pygame.image.load("starry_bg.png")

spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
crystal_img = pygame.transform.scale(crystal_img, (30, 30))
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

asteroid_sizes = {
    "small": pygame.transform.scale(asteroid_img, (30, 30)),
    "medium": pygame.transform.scale(asteroid_img, (50, 50)),
    "large": pygame.transform.scale(asteroid_img, (70, 70))
}

FPS = 60
lives = 3
collected_crystals = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()

font = pygame.font.Font("HomeVideo-BLG6G.ttf", 20)
game_font = pygame.font.Font("HomeVideo-BLG6G.ttf", 40)


def display_text(text, x, y, color=WHITE, font_type=font):
    screen.blit(font_type.render(text, True, color), (x, y))


def game_over():
    screen.fill(BLACK)
    display_text("Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, RED, game_font)
    display_text("Press R to Restart or Q to Quit", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 40, WHITE)
    pygame.display.flip()
    pygame.mixer.music.stop()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_menu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def victory():
    screen.fill(BLACK)
    display_text("You won!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, GREEN, game_font)
    display_text("Press R to Restart or Q to Quit", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 40, WHITE)
    pygame.display.flip()
    pygame.mixer.music.stop()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_menu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main_menu():
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)

    screen.fill(BLACK)
    display_text("Collect your chosen number of energy crystals", 50, 50)
    display_text("and don't get killed by the asteroids", 50, 70)
    display_text("Difficulty:", 50, 150)

    display_text("1. ", 100, 200)
    display_text("Easy", 130, 200, GREEN)
    display_text(" (collect 4 crystals in 10 seconds)", 190, 200)

    display_text("2. ", 100, 250)
    display_text("Medium", 130, 250, YELLOW)
    display_text(" (collect 10 crystals in 20 seconds)", 220, 250)

    display_text("3. ", 100, 300)
    display_text("Hard", 130, 300, RED)
    display_text(" (collect 17 crystals in 30 seconds)", 190, 300)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 100 <= mouse_x <= 400 and 200 <= mouse_y <= 230:
                    game_loop("easy")
                if 100 <= mouse_x <= 400 and 250 <= mouse_y <= 280:
                    game_loop("medium")
                if 100 <= mouse_x <= 400 and 300 <= mouse_y <= 330:
                    game_loop("hard")


def game_loop(difficulty):
    global lives, collected_crystals
    lives = 3
    collected_crystals = 0

    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)

    crystal_target = {"easy": 4, "medium": 10, "hard": 17}[difficulty]
    time_limit = {"easy": 10, "medium": 20, "hard": 30}[difficulty]

    asteroid_difficulty = {
        "easy": [("small",)],
        "medium": [("small",), ("small", "medium")],
        "hard": [("small",), ("small", "medium"), ("small", "medium", "large")]
    }[difficulty]

    spaceship_x = SCREEN_WIDTH // 2
    spaceship_y = SCREEN_HEIGHT - 70

    asteroids = []
    crystals = []

    start_time = pygame.time.get_ticks()

    while True:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            spaceship_x -= 5
            if spaceship_x < -50:
                spaceship_x = SCREEN_WIDTH
        if keys[pygame.K_RIGHT]:
            spaceship_x += 5
            if spaceship_x > SCREEN_WIDTH:
                spaceship_x = -50

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = max(0, int(time_limit - elapsed_time))

        if len(asteroids) < 5:
            size = random.choice(asteroid_difficulty[min(int(elapsed_time // 10), len(asteroid_difficulty) - 1)])
            asteroids.append({"x": random.randint(0, SCREEN_WIDTH - 50), "y": -50, "size": size})

        if len(crystals) < 5 and random.random() < 0.02:
            crystals.append({"x": random.randint(0, SCREEN_WIDTH - 30), "y": -30})

        speed_factor = 1
        if elapsed_time > 10:
            speed_factor = 1.2
        if elapsed_time > 20:
            speed_factor = 1.6

        for asteroid in asteroids[:]:
            asteroid["y"] += int(5 * speed_factor)
            if asteroid["y"] > SCREEN_HEIGHT:
                asteroids.remove(asteroid)
            elif spaceship_x < asteroid["x"] < spaceship_x + 50 and spaceship_y < asteroid["y"] < spaceship_y + 50:
                clash_sound.play()
                lives -= {"small": 1, "medium": 2, "large": 3}[asteroid["size"]]
                asteroids.remove(asteroid)

        for crystal in crystals[:]:
            crystal["y"] += 3
            if crystal["y"] > SCREEN_HEIGHT:
                crystals.remove(crystal)
            elif spaceship_x < crystal["x"] < spaceship_x + 50 and spaceship_y < crystal["y"] < spaceship_y + 50:
                collected_crystals += 1
                crystals.remove(crystal)

        screen.blit(spaceship_img, (spaceship_x, spaceship_y))

        for asteroid in asteroids:
            screen.blit(asteroid_sizes[asteroid["size"]], (asteroid["x"], asteroid["y"]))

        for crystal in crystals:
            screen.blit(crystal_img, (crystal["x"], crystal["y"]))

        display_text(f"Hearts: {lives}", SCREEN_WIDTH - 150, 10)
        display_text(f"Crystals: {collected_crystals}", 10, 10)
        display_text(f"Time: {remaining_time}s", SCREEN_WIDTH // 2 - 110, 10, WHITE, game_font)

        pygame.display.flip()
        clock.tick(FPS)

        if lives <= 0:
            game_over()

        if collected_crystals >= crystal_target:
            victory()

        if elapsed_time >= time_limit:
            game_over()


main_menu()