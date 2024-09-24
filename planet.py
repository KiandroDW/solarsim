import math
import pygame

import orbit
import screen


planets = []


# Main class that calculates everything
class Planet:
    """
    Name: The name of the planet

    StartAngle: The angle between the vernal equinox and the position of the planet in radians at T=0.

    PerihelionDistance: The distance from the star in the planet's perihelion in kilometers.

    perihelionAngle: The angle between the vernal equinox and the perihelion of the planet in radians.

    period: The period of the planet in days.

    eccentricity: how eccentric the ellipse is with 0 < eccentricity < 1.

    radius: The radius of the planet in kilometers.

    color: The color of the planet for the graph in '[R, G, B]'.

    This calculates all elements of the orbit.
    """

    def __init__(self, name: str, start_angle: float, perihelion_distance: float,
                 perihelion_angle: float, period: float, eccentricity: float, radius: float, color: str):
        # Save all the settings of the planet
        self.startA = start_angle
        self.periD = perihelion_distance
        self.periA = perihelion_angle + math.pi
        self.period = period
        self.ecc = eccentricity
        self.radius = radius
        self.color = color
        self.name = name
        planets.append(self)

        self.orbit = orbit.Orbit(self.startA, self.periD, self.periA, self.period, self.ecc)

    # Process updates the image with newly calculated coordinates for the planets
    def process(self):
        self.orbit.position = [self.orbit.x / orbit.scale + int(screen.window_dim[0]) / 2, self.orbit.y / orbit.scale + int(screen.window_dim[1]) / 2]
        pygame.draw.circle(screen.screen, self.color, self.orbit.position, radius=self.radius / orbit.rscale)
        pygame.draw.polygon(screen.screen, self.color, self.orbit.orbit_list, width=5)
        gm = 6.67e-11 * 1.989e30
        velocity = math.sqrt(gm * (2 / (math.sqrt(self.orbit.x ** 2 + self.orbit.y ** 2) * 1000) - 1 / (self.orbit.semi_major_axis * 1000)))
        avelocity = velocity / math.sqrt((self.orbit.x * 1000) ** 2 + (self.orbit.y * 1000) ** 2) * screen.spf
        self.orbit.totalw += avelocity
        self.orbit.x = self.orbit.semi_major_axis * math.cos(- self.periA - self.startA + self.orbit.angle_diff - self.orbit.totalw) \
            * math.cos(self.periA) - \
            self.orbit.semi_major_axis * math.sin(- self.periA - self.startA + self.orbit.angle_diff - self.orbit.totalw) \
            * math.sin(self.periA) - self.orbit.cx
        self.orbit.y = self.orbit.semi_major_axis * math.cos(- self.periA - self.startA + self.orbit.angle_diff - self.orbit.totalw) \
            * math.sin(self.periA) + \
            self.orbit.semi_minor_axis * math.sin(- self.periA - self.startA + self.orbit.angle_diff - self.orbit.totalw) \
            * math.cos(self.periA) - self.orbit.cy
