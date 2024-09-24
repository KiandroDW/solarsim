import math
import pygame

modechanging = False
# Create a popup screen and loading screen
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
font = pygame.font.SysFont('Arial', 20)
windowdim = pygame.display.get_window_size()
screen.fill((0, 0, 0))
ltext = font.render("Loading...", True, [255, 255, 255], [0, 0, 0])
ltextRect = ltext.get_rect()
ltextRect.center = (500, 500)
screen.blit(ltext, ltextRect)
pygame.display.flip()
spf = 3600
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
        self.name = name
        self.radius = radius
        self.color = color
        planets.append(self)

        # Define the different scales for the mode
        self.scale = 600000
        self.rscale = 200
        self.solarradius = 40

        # semi-major axis, semi-minor axis
        self.Major = self.periD / (1 - self.ecc)
        self.Minor = math.sqrt(-(self.ecc ** 2 - 1) * self.Major ** 2)

        # periC is the coordinates of the perihelion
        peri_coords = [self.periD * math.cos(self.periA),
                       self.periD * math.sin(self.periA)]

        # Calculate the orbit
        x, y = [], []
        t = 0
        self.cx = self.Major * math.cos(self.periA) - peri_coords[0]
        self.cy = self.Major * math.sin(self.periA) - peri_coords[1]
        while t < 6.3:
            x.append(self.Major * math.cos(t) * math.cos(self.periA) -
                     self.Minor * math.sin(t) * math.sin(self.periA) - self.cx)
            y.append(self.Major * math.cos(t) * math.sin(self.periA) +
                     self.Minor * math.sin(t) * math.cos(self.periA) - self.cy)
            t += 0.063

        # Save the coordinates for the drawing tool
        self.coords = []
        for j in x:
            pos = x.index(j)
            self.coords.append((x[pos] / self.scale + int(windowdim[0]) / 2, y[pos] / self.scale + int(windowdim[1]) / 2))

        # Calculate the x-coordinate of the planet when it's at y=0
        closesty = min([math.fabs(j) for j in y])
        if closesty not in y:
            closesty = - closesty
        place = y.index(closesty)
        if x[place] < 0:
            y.remove(closesty)
            closesty2 = min([math.fabs(j) for j in y])
            if closesty2 not in y:
                closesty2 = - closesty2
            place = y.index(closesty2)
        closestx = x[place]
        self.closestx = closestx

        # Use this x-coordinate to find the angle from the center at which the planet is at that position
        if math.pi / 2 < perihelion_angle < 3 * math.pi / 2:
            a = self.Major - self.periD
            r = math.sqrt(a ** 2 + closestx ** 2 - 2 * a * closestx * math.cos(math.pi - self.periA))
            self.Anglediff = self.periA - (math.asin(closestx * math.sin(math.pi - self.periA) / r))
        else:
            a = self.Major - self.periD
            r = math.sqrt(a ** 2 + closestx ** 2 - 2 * a * closestx * math.cos(2 * math.pi - self.periA))
            self.Anglediff = math.pi - self.periA + (math.asin(closestx * math.sin(2 * math.pi - self.periA) / r))

        # Calculate the position of the planet at the start
        self.x = self.Major * math.cos(- self.periA - self.startA + self.Anglediff) * math.cos(self.periA) - \
            self.Minor * math.sin(- self.periA - self.startA + self.Anglediff) * math.sin(self.periA) - self.cx
        self.y = self.Major * math.cos(- self.periA - self.startA + self.Anglediff) * math.sin(self.periA) + \
            self.Minor * math.sin(- self.periA - self.startA + self.Anglediff) * math.cos(self.periA) - self.cy

        self.position = [self.x / self.scale + int(windowdim[0]) / 2, self.y / self.scale + int(windowdim[1]) / 2]
        self.outerposition = [0, 0]

        # Calculate the error-factor on the position of the planet, this error happens because this program calculates
        # the angular velocity manually
        totalw = 0
        for _ in range(int(self.period * 24)):
            x = self.Major * math.cos(- self.periA - self.startA + self.Anglediff - totalw) * math.cos(self.periA) - \
                self.Minor * math.sin(- self.periA - self.startA + self.Anglediff - totalw) * math.sin(
                self.periA) - self.cx
            y = self.Major * math.cos(- self.periA - self.startA + self.Anglediff - totalw) * math.sin(self.periA) + \
                self.Minor * math.sin(- self.periA - self.startA + self.Anglediff - totalw) * math.cos(
                self.periA) - self.cy
            gm = 6.67e-11 * 1.989e30
            velocity = math.sqrt(gm * (2 / (math.sqrt(x ** 2 + y ** 2) * 1000) - 1 / (self.Major * 1000)))
            avelocity = velocity / math.sqrt((x * 1000) ** 2 + (y * 1000) ** 2) * 3600
            totalw += avelocity
        self.errorf = (2 * math.pi) / totalw
        self.totalw = 0

    # Process updates the image with newly calculated coordinates for the planets
    def process(self):
        self.position = [self.x / self.scale + int(windowdim[0]) / 2, self.y / self.scale + int(windowdim[1]) / 2]
        pygame.draw.circle(screen, self.color, self.position, radius=self.radius / self.rscale)
        pygame.draw.polygon(screen, self.color, self.coords, width=5)
        gm = 6.67e-11 * 1.989e30
        velocity = math.sqrt(gm * (2 / (math.sqrt(self.x ** 2 + self.y ** 2) * 1000) - 1 / (self.Major * 1000)))
        avelocity = velocity / math.sqrt((self.x * 1000) ** 2 + (self.y * 1000) ** 2) * spf * self.errorf
        self.totalw += avelocity
        self.x = self.Major * math.cos(- self.periA - self.startA + self.Anglediff - self.totalw) \
            * math.cos(self.periA) - \
            self.Minor * math.sin(- self.periA - self.startA + self.Anglediff - self.totalw) \
            * math.sin(self.periA) - self.cx
        self.y = self.Major * math.cos(- self.periA - self.startA + self.Anglediff - self.totalw) \
            * math.sin(self.periA) + \
            self.Minor * math.sin(- self.periA - self.startA + self.Anglediff - self.totalw) \
            * math.cos(self.periA) - self.cy
