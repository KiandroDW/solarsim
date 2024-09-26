import math
import pygame

import screen

bodies = []


class Body:
    def __init__(self, positional_data: list[list[float]],
                 radius: float,
                 color: tuple[int, int, int],
                 dist_fact: float,
                 x_fact: float,
                 y_fact: float,
                 radius_fact: float) -> None:
        """
        Create a celestial body

        positional_data: list of points of the polar coordinates of the body  [angle in degrees, distance in AU]
        radius: radius of the body
        color: color of the body
        *_fact: scaling factor for the specific datapoint, this uses either the x- or y-dimension of your screen
            dist_fact: factor for the radius of the orbit (uses y-dimension)
            x_fact: factor for the x-coordinate of the orbit center (uses x-dimension)
            y_fact: factor for the y-coordinate of the orbit center (uses y-dimension)
            radius_fact: factor for the radius of the body (uses y-dimension)
        """
        # Unpack data to x and y coordinates
        self.data = []
        for data in positional_data:
            x = data[1] * math.cos(math.radians(data[0])) * int(screen.WINDOW_DIM[1]) / dist_fact
            y = - data[1] * math.sin(math.radians(data[0])) * int(screen.WINDOW_DIM[1]) / dist_fact
            self.data.append((x, y))

        self.radius = radius / 1000
        self.color = color

        self.x_fact = x_fact
        self.y_fact = y_fact
        self.radius_fact = radius_fact
        bodies.append(self)

    def process(self):
        # For each point of data, it draws a small circle.
        # The last point of data is the body, so it gets a bigger circle.
        for index, data in enumerate(self.data):
            radius = self.radius * (screen.WINDOW_DIM[1] / self.radius_fact) if index == 99 else 3
            pygame.draw.circle(screen.screen, [int(value * index / 100) for value in self.color],
                               [data[0] + int(screen.WINDOW_DIM[0]) / self.x_fact,
                                data[1] + int(screen.WINDOW_DIM[1]) / self.y_fact],
                               radius)

