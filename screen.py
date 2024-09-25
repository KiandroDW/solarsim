import pygame
import sys

# Create a popup screen
pygame.init()
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_dim = pygame.display.get_window_size()
screen.fill((0, 0, 0))
pygame.display.flip()
FPS = 10
SPF = 0.1


def start(planets):
    # Draw the image repeatedly.
    while True:
        screen.fill((0, 0, 0))
        # Close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the sun and every planet
        for planet in planets:
            planet.process()
        pygame.draw.circle(screen, [255, 242, 222], (int(window_dim[0]) / 2, int(window_dim[1]) / 2),
                           radius=20)
        pygame.display.flip()
        fps_clock.tick(FPS)
