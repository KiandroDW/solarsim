import pygame
import random


# Initialize the screen and constants
pygame.init()
FPS = 10
SPF = 0.1
screen = None
WINDOW_DIM = pygame.display.Info().current_w, pygame.display.Info().current_h
stars = []


def start(planets) -> None:
    global screen
    # Create a popup screen
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.NOFRAME)
    screen.fill((0, 0, 0))
    pygame.display.flip()

    generate_stars()
    # Draw the bodies repeatedly.
    while True:
        screen.fill((0, 0, 0))

        # Close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        # Draw all the stars
        for star in stars:
            pygame.draw.circle(screen, [star[2], star[3], star[4]], [star[0], star[1]], 1)

        # Draw the bodies
        for planet in planets:
            planet.process()
        # Draw the sun in the main screen
        pygame.draw.circle(screen, [255, 242, 222], (int(WINDOW_DIM[0]) / 3, int(WINDOW_DIM[1]) / 2),
                           radius=int(WINDOW_DIM[1]) / 50)
        # Draw the sun in the top right screen
        pygame.draw.circle(screen, [255, 242, 222], (int(WINDOW_DIM[0]) / (6 / 5), int(WINDOW_DIM[1]) / 4),
                           radius=int(WINDOW_DIM[1]) / 100)
        # Draw the earth in the bottom right screen
        pygame.draw.circle(screen, [85, 101, 131], (int(WINDOW_DIM[0]) / (6 / 5), int(WINDOW_DIM[1]) / (4 / 3)),
                           radius=int(WINDOW_DIM[1]) / 25)
        pygame.display.flip()
        fps_clock.tick(FPS)


def generate_stars() -> None:
    """
    Generate 400 randomly placed stars which have varying brightness and color.
    """
    for i in range(400):
        # random position
        x = random.randint(1, WINDOW_DIM[0])
        y = random.randint(1, WINDOW_DIM[1])

        # random color which is either more blue or red
        change = random.randint(-15, 15) * 5
        r = 255 - abs(change) if change < 0 else 255
        g = 255 - abs(change)
        b = 255 - abs(change) if change > 0 else 255

        # random brightness
        brightness = random.randint(1, 7) * random.randint(1, 10) * 0.01
        stars.append((x, y, r * brightness, g * brightness, b * brightness))
