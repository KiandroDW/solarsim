import pygame
import sys
import random


pygame.init()
FPS = 10
SPF = 0.1
screen = None
window_dim = pygame.display.Info().current_w, pygame.display.Info().current_h
stars = []


def start(planets):
    global screen
    # Create a popup screen
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.NOFRAME)
    screen.fill((0, 0, 0))
    pygame.display.flip()

    generate_stars()
    # Draw the image repeatedly.
    while True:
        screen.fill((0, 0, 0))
        # Close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for star in stars:
            pygame.draw.circle(screen, [star[2], star[3], star[4]], [star[0], star[1]], 1)

        # Draw the sun and every planet
        for planet in planets:
            planet.process()
        pygame.draw.circle(screen, [255, 242, 222], (int(window_dim[0]) / 3, int(window_dim[1]) / 2),
                           radius=int(window_dim[1]) / 50)
        pygame.draw.circle(screen, [255, 242, 222], (int(window_dim[0]) / (6 / 5), int(window_dim[1]) / 4),
                           radius=int(window_dim[1]) / 100)
        pygame.draw.circle(screen, [85, 101, 131], (int(window_dim[0]) / (6 / 5), int(window_dim[1]) / (4 / 3)),
                           radius=int(window_dim[1]) / 50)
        pygame.display.flip()
        fps_clock.tick(FPS)


def generate_stars():
    for i in range(400):
        x = random.randint(1, window_dim[0])
        y = random.randint(1, window_dim[1])
        change = random.randint(-15, 15) * 5
        r = 255 - abs(change) if change < 0 else 255
        g = 255 - abs(change)
        b = 255 - abs(change) if change > 0 else 255

        brightness = random.randint(1, 7) * random.randint(1, 10) * 0.01
        stars.append((x, y, r * brightness, g * brightness, b * brightness))
