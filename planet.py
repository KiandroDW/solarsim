import math
import pygame

import screen

planets = []


class Planet:
    def __init__(self, date, hour, lat, r, radius, color):
        self.date = date
        self.hour = hour
        self.lat = lat
        self.r = float(r)
        self.radius = float(radius)
        self.color = color

        self.x = self.r * math.cos(math.radians(float(self.lat)))
        self.y = - self.r * math.sin(math.radians(float(self.lat)))
        planets.append(self)

    def process(self):
        pygame.draw.circle(screen.screen, self.color, [self.x * 300 + int(screen.window_dim[0]) / 2, self.y * 300 + int(screen.window_dim[1]) / 2], self.radius / 200)
