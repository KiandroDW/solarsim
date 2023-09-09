import math
import json
import datetime
import pygame
import sys
from pygame.math import Vector2
import ctypes

# Create a popup screen
ctypes.windll.shcore.SetProcessDpiAwareness(1)
pygame.init()
fpsClock = pygame.time.Clock()
windowdim = Vector2(1500, 1000)
screen = pygame.display.set_mode((int(windowdim.x), int(windowdim.y)), pygame.RESIZABLE)


# RefDay is the day + hour of which the simulation is based
RefDay = datetime.datetime(2023, 3, 20, 22)
Today = datetime.datetime(datetime.datetime.today().year,
                          datetime.datetime.today().month,
                          datetime.datetime.today().day,
                          datetime.datetime.today().hour)


# Main class that calculates everything
class Planet:
    """
    Name: The name of the planet

    StartAngle: The angle between the vernal equinox and the position of the planet in radians at T=0.

    PerihelionDistance: The distance from the star in the planet's perihelion in kilometers.

    perihelionAngle: The angle between the vernal equinox and the perihelion of the planet in radians.

    period: The period of the planet in days.

    eccentricity: how eccentric the ellips is with 0 < eccentricity < 1.

    radius: The radius of the planet in kilometers.

    color: The color of the planet for the graph in '[R, G, B]'.

    This calculates all elements of the orbit.
    """
    def __init__(self, Name: str, StartAngle: float, PerihelionDistance: float,
                  PerihelionAngle: float, period: float, eccentricity: float, radius: float, color: str):
        # Save all the settings of the planet
        self.startA = StartAngle
        self.periD = PerihelionDistance
        self.periA = PerihelionAngle + math.pi
        self.period = period
        self.ecc = eccentricity
        self.name = Name
        self.radius = radius
        colorl = color.replace("[", "").replace("]", "").split(", ")
        colorl = [int(i) for i in colorl]
        self.color = colorl
        planets.append(self)

        # semi-major axis, semi-minor axis
        self.Major = self.periD / (1 - self.ecc)
        self.Minor = math.sqrt(-(self.ecc ** 2 - 1) * self.Major ** 2)

        # periC is the coordinates of the perihelion
        periC = [self.periD * math.cos(self.periA),
                 self.periD * math.sin(self.periA)]

        # Calculate the orbit
        x, y = [], []
        t = 0
        self.cx = self.Major * math.cos(self.periA) - periC[0]
        self.cy = self.Major * math.sin(self.periA) - periC[1]
        while t < 6.3:
            x.append(self.Major * math.cos(t) * math.cos(self.periA) -
                     self.Minor * math.sin(t) * math.sin(self.periA) - self.cx)
            y.append(self.Major * math.cos(t) * math.sin(self.periA) +
                     self.Minor * math.sin(t) * math.cos(self.periA) - self.cy)
            t += 0.01

        # Save the coordinates for the drawing tool
        self.coords = []
        for i in x:
            pos = x.index(i)
            self.coords.append((x[pos] / 500000 + 750, y[pos] / 500000 + 500))

        # Calculate the x-coordinate of the planet when it's at y=0
        closesty = min([math.fabs(i) for i in y])
        if closesty not in y:
            closesty = - closesty
        place = y.index(closesty)
        if x[place] < 0:
            y.remove(closesty)
            closesty2 = min([math.fabs(i) for i in y])
            if closesty2 not in y:
                closesty2 = - closesty2
            place = y.index(closesty2)
        closestx = x[place]
        self.closestx = closestx

        # Use this x-coordinate to find the angle from the center at which the planet is at that position
        if math.pi / 2 < PerihelionAngle < 3 * math.pi / 2:
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

        # Calculate the error-factor on the position of the planet, this error happens because this program calculates
        # the angular velocity manually
        totalw = 0
        for i in range(int(self.period * 24)):
            x = self.Major * math.cos(- self.periA - self.startA + self.Anglediff - totalw) * math.cos(self.periA) - \
                self.Minor * math.sin(- self.periA - self.startA + self.Anglediff - totalw) * math.sin(self.periA) - self.cx
            y = self.Major * math.cos(- self.periA - self.startA + self.Anglediff - totalw) * math.sin(self.periA) + \
                self.Minor * math.sin(- self.periA - self.startA + self.Anglediff - totalw) * math.cos(self.periA) - self.cy
            GM = 6.67e-11 * 1.989e30
            velocity = math.sqrt(GM * (2 / (math.sqrt(x ** 2 + y ** 2) * 1000) - 1 / (self.Major * 1000)))
            avelocity = velocity / math.sqrt((x * 1000) ** 2 + (y * 1000) ** 2) * 3600
            totalw += avelocity
        self.errorf = (2 * math.pi) / totalw

        # Process updates the image with newly calculated coordinates for the planets
        self.totalw = 0

    def process(self):
        pygame.draw.polygon(screen, self.color, self.coords, width=5)
        pygame.draw.circle(screen, self.color, (self.x / 500000 + 750, self.y / 500000 + 500), radius=self.radius / 200)
        GM = 6.67e-11 * 1.989e30
        velocity = math.sqrt(GM * (2 / (math.sqrt(self.x ** 2 + self.y ** 2) * 1000) - 1 / (self.Major * 1000)))
        avelocity = velocity / math.sqrt((self.x * 1000) ** 2 + (self.y * 1000) ** 2) * spf * self.errorf
        self.totalw += avelocity
        self.x = self.Major * math.cos(- self.periA - self.startA + self.Anglediff - self.totalw) * math.cos(self.periA) - \
                 self.Minor * math.sin(- self.periA - self.startA + self.Anglediff - self.totalw) * math.sin(self.periA) - self.cx
        self.y = self.Major * math.cos(- self.periA - self.startA + self.Anglediff - self.totalw) * math.sin(self.periA) + \
                 self.Minor * math.sin(- self.periA - self.startA + self.Anglediff - self.totalw) * math.cos(self.periA) - self.cy


# Open the json file with all the date of the planets
with open('planetdata.json') as json_file:
    data = json.load(json_file)

# Call the planet class on all the planets
planets = []
for planet in data:
    Planet(data[planet]["Name"],
           float(data[planet]["Start Angle"]),
           float(data[planet]["Perihelion Distance"]),
           float(data[planet]["Perihelion Angle"]),
           float(data[planet]["Period"]),
           float(data[planet]["Eccentricity"]),
           float(data[planet]["Radius"]),
           data[planet]["Color"],
           )

# Draw the image repeatedly.
spf = 3600
while True:
    screen.fill((0, 0, 0))
    # Close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print(f'Refday = {RefDay}')
            for p in planets:
                print(f'Start Angle {p.name} = {p.startA + p.totalw}')
            sys.exit()

    # Draw the sun and every planet
    for p in planets:
        p.process()
        pygame.draw.circle(screen, [255, 242, 222], (750, 500), radius=40)

    # Makes the movement fast until the planets are at their current positions
    if RefDay < Today:
        fps = 120
        RefDay = RefDay + datetime.timedelta(minutes=60)
    else:
        fps = 1
        spf = 1
        RefDay = RefDay + datetime.timedelta(seconds=1)

    pygame.display.flip()
    fpsClock.tick(fps)


# Mercurius = Planet(0.1698205362, 46001195.6, 1.351862225, 87.9691, 0.205630)
# Venus = Planet(1.5123277970, 107477094, 2.296224977, 224.701, 0.006772)
# Aarde = Planet(3.141592654, 146605913, 1.796589572, 356.256, 0.016710219)
# Mars = Planet(2.211157629, 206744257.29, 5.874900435, 686.971, 0.0934)
# Jupiter = Planet(0, 740599219, 0.2501231351, 4332.59, 0.0489, [184, 163, 110])
# Saturnus = Planet(0, 1352544268.6, 1.624151042, 10755.70, 0.0565, [214, 191, 150])
# Uranus = Planet(0, 2735561623.4, 3.019506872, 30688.5, 0.04717, [164, 191, 191])
# Neptunus = Planet(0, 4459512525.6, 0.8399222492, 60195, 0.008678, [127, 155 212])
# Pluto = Planet(0, 4436773649.2, 3.910846521, 90560, 0.2488, [200, 163, 132])  # niet echt

# plt.plot(Mercurius.ellipsex, Mercurius.ellipsey, color='k')
# plt.plot(Venus.ellipsex, Venus.ellipsey, color='y')
# plt.plot(Aarde.ellipsex, Aarde.ellipsey, color='b')
# plt.plot(Mars.ellipsex, Mars.ellipsey, color='r')
# plt.plot(Jupiter.ellipsex, Jupiter.ellipsey, color='y')
# plt.plot(Saturnus.ellipsex, Saturnus.ellipsey, color='y')
# plt.plot(Uranus.ellipsex, Uranus.ellipsey, color='c')
# plt.plot(Neptunus.ellipsex, Neptunus.ellipsey, color='b')
# plt.plot(Pluto.ellipsex, Pluto.ellipsey, color='k')


# sun = plt.Circle((0, 0), 10000000, color='y')
# earth = plt.Circle((Aarde.x, Aarde.y), 10000000, color='b')
# ax.add_patch(sun)
# ax.add_patch(earth)



