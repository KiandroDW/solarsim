import math
import json
import datetime
import pygame
import sys
from pygame.math import Vector2
import ctypes

# Choose if you want to see the "INNER" or "OUTER" planets
mode = "INNER"
# Choose if you want to see the outer planets on "INNER" mode
outervis = False
# You can change these settings inside the simulation
# The filename of the JSON file with planet-data
filename = "planetdata.json"
# RefDay: (year, month, date, hour) is the time on which the simulation is based. If you change it,
# change the Start Angle in the JSON file to the correct angle on that date if you want it to be accurate
RefDay = datetime.datetime(2023, 3, 20, 22)
# These 4 are the only things you should change to not brake it

Today = datetime.datetime(datetime.datetime.today().year,
                          datetime.datetime.today().month,
                          datetime.datetime.today().day,
                          datetime.datetime.today().hour)
modechanging = False
starting = False
totalmouse = 0
# Create a popup screen and loading screen
ctypes.windll.shcore.SetProcessDpiAwareness(1)
pygame.init()
fpsClock = pygame.time.Clock()
windowdim = Vector2(1000, 1000)
screen = pygame.display.set_mode((int(windowdim.x), int(windowdim.y)), pygame.RESIZABLE)
font = pygame.font.SysFont('Arial', 20)
pygame.display.set_caption('Solarsystem simulator')


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
        colorl = color.replace("[", "").replace("]", "").split(", ")
        colorl = [int(j) for j in colorl]
        self.color = colorl
        planets.append(self)

        # Define the different scales for the mode
        if mode == "INNER":
            self.scale = 600000
            self.rscale = 200
            self.solarradius = 40
        elif mode == "OUTER":
            self.scale = 10000000
            self.rscale = 3000
            self.solarradius = 30
        else:
            assert 1 == 0, "Wrong mode, choose 'INNER' or 'OUTER'"

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
            t += 0.01

        # Save the coordinates for the drawing tool
        self.coords = []
        for j in x:
            pos = x.index(j)
            self.coords.append((x[pos] / self.scale + int(windowdim.x) / 2, y[pos] / self.scale + int(windowdim.y) / 2))

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

        self.position = [self.x / self.scale + int(windowdim.x) / 2, self.y / self.scale + int(windowdim.y) / 2]
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
        self.scale = -313333.3333333333333 * totalmouse + 600000
        self.rscale = -93.33333333333 * totalmouse + 200
        self.solarradius = 12 / (1 + math.e ** (- (totalmouse + 15) / 6)) + 29

        # If you change the mode, the orbits  get recalculated
        global modechanging
        if modechanging:
            x, y = [], []
            t = 0
            while t < 6.3:
                x.append(self.Major * math.cos(t) * math.cos(self.periA) -
                         self.Minor * math.sin(t) * math.sin(self.periA) - self.cx)
                y.append(self.Major * math.cos(t) * math.sin(self.periA) +
                         self.Minor * math.sin(t) * math.cos(self.periA) - self.cy)
                t += 0.01
            self.coords = []
            for j in x:
                pos = x.index(j)
                self.coords.append((x[pos] / self.scale + int(windowdim.x) / 2,
                                    y[pos] / self.scale + int(windowdim.y) / 2))

        # Add the outer planets to the inner planet mode if the setting is enabled
        if ((self.x / self.scale + int(windowdim.x) / 2) > 1000 or (self.x / self.scale + int(windowdim.x) / 2) < 0
            or (self.y / self.scale + int(windowdim.y) / 2) > 1000 or (self.y / self.scale + int(windowdim.y) / 2) < 0)\
                and outervis:
            if (0 <= ((self.startA + self.totalw) % (2 * math.pi)) <= math.pi / 4) or \
                    (7 * math.pi / 4 <= ((self.startA + self.totalw) % (2 * math.pi)) <= 2 * math.pi):
                self.outerposition = [975, - 475 * math.tan(self.startA + self.totalw) + 500]
            elif math.pi / 4 <= ((self.startA + self.totalw) % (2 * math.pi)) <= 3 * math.pi / 4:
                self.outerposition = [475 / math.tan(self.startA + self.totalw) + 500, 25]
            elif 3 * math.pi / 4 <= ((self.startA + self.totalw) % (2 * math.pi)) <= 5 * math.pi / 4:
                self.outerposition = [25, 475 * math.tan(self.startA + self.totalw) + 500]
            else:
                self.outerposition = [- 475 / math.tan(self.startA + self.totalw) + 500, 975]
            if self.name == "Mars":
                pygame.draw.circle(screen, self.color, self.outerposition, radius=self.radius / 2000)
            else:
                pygame.draw.circle(screen, self.color, self.outerposition, radius=self.radius / 3000)
        self.position = [self.x / self.scale + int(windowdim.x) / 2, self.y / self.scale + int(windowdim.y) / 2]
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


objects = []


# The class to make buttons visual and work
class Button:
    def __init__(self, x, y, width, height, button_text='Button', onclick_function=None, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclick_function
        self.onePress = one_press
        self.buttonText = button_text

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
            'press': '#444444'
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(button_text, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mouse_pos = pygame.mouse.get_pos()

        if self.buttonText != 'Start' or not starting:
            if (mode == "INNER" and self.buttonText == 'Outer planets') or \
                    (mode == "OUTER" and self.buttonText == 'Inner planets'):
                self.buttonSurface.fill(self.fillColors['normal'])
            elif (mode == "INNER" and self.buttonText == 'Inner planets') or \
                    (mode == "OUTER" and self.buttonText == 'Outer planets') or \
                    (outervis and self.buttonText == 'Show outer'):
                self.buttonSurface.fill(self.fillColors['press'])
            else:
                self.buttonSurface.fill(self.fillColors['normal'])
            if self.buttonRect.collidepoint(mouse_pos):
                self.buttonSurface.fill(self.fillColors['hover'])

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.buttonSurface.fill(self.fillColors['pressed'])

                    if self.onePress:
                        self.onclickFunction()

                    elif not self.alreadyPressed:
                        self.onclickFunction()
                        self.alreadyPressed = True

                else:
                    self.alreadyPressed = False

            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
                self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
            ])
            screen.blit(self.buttonSurface, self.buttonRect)


# Functions the buttons have to do
def modechange(m):
    global mode
    global modechanging
    global totalmouse
    if m == 1:
        mode = "OUTER"
        totalmouse = -30
    else:
        mode = "INNER"
        totalmouse = 0
    modechanging = True


def outervisual(_):
    global outervis
    if outervis:
        outervis = False
    else:
        outervis = True


def start(_):
    global starting
    starting = True


buttons = [
    ['Inner planets', lambda: modechange(0)],
    ['Outer planets', lambda: modechange(1)],
    ['Show outer', lambda: outervisual(0)],
    ['Start', lambda: start(0)]
]


buttonWidth = 120
buttonHeight = 35

for index, buttonName in enumerate(buttons):
    Button(440, index * (buttonHeight + 10) + 415, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])

while not starting:
    screen.fill((0, 0, 0))
    # Close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for i in objects:
        i.process()

    ltext = font.render("Choose presets, these can be changed inside the simulation", True, [255, 255, 255], [0, 0, 0])
    ltextRect = ltext.get_rect()
    ltextRect.center = (500, 375)
    screen.blit(ltext, ltextRect)

    pygame.display.flip()
    fpsClock.tick(60)

screen.fill((0, 0, 0))
objects = []

ltext = font.render("Loading...", True, [255, 255, 255], [0, 0, 0])
ltextRect = ltext.get_rect()
ltextRect.center = (500, 500)
screen.blit(ltext, ltextRect)
pygame.display.flip()


for index, buttonName in enumerate(buttons):
    Button(index * (buttonWidth + 10) + 10, 10, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])

# Open the json file with all the date of the planets
with open(filename) as json_file:
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


# Display the names of the planets when you hover over them
def planetnames(pl):
    mouspos = pygame.mouse.get_pos()
    if math.fabs(mouspos[0] - 500) < pl.solarradius and math.fabs(mouspos[1] - 500) < pl.solarradius:
        text = font.render("Sun", True, [255, 255, 255], [0, 0, 0])
        text_rect = text.get_rect()
        text_rect.center = (100, 100)
        screen.blit(text, text_rect)
    elif math.fabs(mouspos[0] - pl.position[0]) < pl.radius / pl.rscale and \
            math.fabs(mouspos[1] - pl.position[1]) < pl.radius / pl.rscale:
        text = font.render(pl.name, True, [255, 255, 255], [0, 0, 0])
        text_rect = text.get_rect()
        text_rect.center = (100, 100)
        screen.blit(text, text_rect)
    elif math.fabs(mouspos[0] - pl.outerposition[0]) < pl.radius / 3000 and \
            math.fabs(mouspos[1] - pl.outerposition[1]) < pl.radius / 3000:
        text = font.render(pl.name, True, [255, 255, 255], [0, 0, 0])
        text_rect = text.get_rect()
        text_rect.center = (100, 100)
        screen.blit(text, text_rect)
    elif pl.name == "Mars" and (math.fabs(mouspos[0] - pl.outerposition[0]) < pl.radius / 100 and
                                math.fabs(mouspos[1] - pl.outerposition[1]) < pl.radius / 100):
        text = font.render(pl.name, True, [255, 255, 255], [0, 0, 0])
        text_rect = text.get_rect()
        text_rect.center = (100, 100)
        screen.blit(text, text_rect)


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
                print(f'Start Angle {p.name} = {(p.startA + p.totalw) % (2 * math.pi)}')
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            totalmouse += event.y
            if totalmouse > 1:
                totalmouse = 1
            elif totalmouse < -200:
                totalmouse = -200
            if totalmouse == 0:
                mode = "INNER"
            elif totalmouse == -30:
                mode = "OUTER"
            else:
                mode = "Custom"
            modechanging = True

    # Draw the sun and every planet
    for p in planets:
        p.process()
        planetnames(p)
        pygame.draw.circle(screen, [255, 242, 222], (int(windowdim.x) / 2, int(windowdim.y) / 2), radius=p.solarradius)
    modechanging = False

    # Draw the buttons
    for i in objects:
        i.process()

    # Makes the movement fast until the planets are at their current positions
    if RefDay < Today:
        fps = 120
        RefDay = RefDay + datetime.timedelta(minutes=60)
    else:
        fps = 10
        spf = 0.1
        RefDay = RefDay + datetime.timedelta(seconds=1)

    pygame.display.flip()
    fpsClock.tick(fps)
