import math
import pygame

import screen

planets = []


class Planet:
    def __init__(self, lat, r, radius, color, dist_fact, x_fact, y_fact, r_fact):
        lat = float(lat)
        r = float(r)

        self.radius = float(radius)
        self.color = color

        self.x_fact = x_fact
        self.y_fact = y_fact
        self.r_fact = r_fact

        self.x = r * math.cos(math.radians(lat)) * int(screen.window_dim[1]) / dist_fact
        self.y = - r * math.sin(math.radians(lat)) * int(screen.window_dim[1]) / dist_fact
        planets.append(self)

    def process(self):
        pygame.draw.circle(screen.screen, self.color,
                           [self.x + int(screen.window_dim[0]) / self.x_fact,
                            self.y + int(screen.window_dim[1]) / self.y_fact],
                           self.radius / (screen.window_dim[1] / self.r_fact))
