import pygame
import sys
from math import pi
import datetime

# Create a popup screen
pygame.init()
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_dim = pygame.display.get_window_size()
screen.fill((0, 0, 0))
pygame.display.flip()
spf = 3600


def start(ref_day, planets):
    # Draw the image repeatedly.
    while True:
        global spf
        screen.fill((0, 0, 0))
        # Close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print(f'Refday = {ref_day}')
                for planet in planets:
                    print(f'Start Angle {planet.name} = {(planet.orbit.start_angle + planet.orbit.totalw) % (2 * pi)}')
                sys.exit()

        # Draw the sun and every planet
        for planet in planets:
            planet.process()
        pygame.draw.circle(screen, [255, 242, 222], (int(window_dim[0]) / 2, int(window_dim[1]) / 2),
                           radius=30)

        # Makes the movement fast until the planets are at their current positions
        if ref_day < datetime.datetime.today():
            fps = 120
            ref_day = ref_day + datetime.timedelta(minutes=60)
        else:
            fps = 10
            spf = 0.1
            ref_day = ref_day + datetime.timedelta(seconds=1)

        pygame.display.flip()
        fps_clock.tick(fps)
