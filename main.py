import math
import time

import matplotlib.pyplot as plt
import json
import datetime


RefDay = datetime.datetime(1999, 1, 1, 0, 1)
Today = datetime.datetime.today()


def dayscalc(startday, endday):
    delta = endday - startday
    return delta.days + (delta.seconds / 86400)


class Planet:
    """
    StartAngle: The angle between the vernal equinox and the position of the planet in radians at T=0.

    PerihelionDistance: The distance from the star in the planet's perihelion in kilometers.

    perihelionAngle: The angle between the vernal equinox and the perihelion of the planet in radians.

    period: The period of the planet in days.

    eccentricity: how eccentric the ellips is with 0 < eccentricity < 1.

    This calculates all elements of the orbit.
    """
    def __init__(self, StartAngle: float, PerihelionDistance: float,
                  PerihelionAngle: float, period: float, eccentricity: float):
        self.startA = StartAngle
        self.periD = PerihelionDistance
        self.periA = PerihelionAngle + math.pi
        self.period = period
        self.ecc = eccentricity

        # semi-major axis, semi-minor axis, circumference
        self.Major = self.periD / (1 - self.ecc)
        self.Minor = math.sqrt(-(self.ecc ** 2 - 1) * self.Major ** 2)
        h = ((self.Major - self.Minor) ** 2) / ((self. Major + self.Minor) ** 2)
        self.circ = math.pi * (self.Major + self.Minor) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))

        periC = [self.periD * math.cos(self.periA),
                 self.periD * math.sin(self.periA)]
        # function
        x, y = [], []
        t = 0
        self.cx = self.Major * math.cos(self.periA) - periC[0]
        self.cy = self.Major * math.sin(self.periA) - periC[1]
        while t < 6.3:
            x.append(self.Major * math.cos(t) * math.cos(self.periA) -
                     self.Minor * math.sin(t) * math.sin(self.periA) + self.cx)
            y.append(self.Major * math.cos(t) * math.sin(self.periA) +
                     self.Minor * math.sin(t) * math.cos(self.periA) + self.cy)
            t += 0.1
        self.ellipsex, self.ellipsey = tuple(x), tuple(y)
        coords = []
        for i in x:
            pos = x.index(i)
            coords.append((x[pos], y[pos]))

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
        if math.pi / 2 < PerihelionAngle < 3 * math.pi / 2:
            a = self.Major - self.periD
            r = math.sqrt(a ** 2 + closestx ** 2 - 2 * a * closestx * math.cos(math.pi - self.periA))
            self.Anglediff = self.periA - (math.asin(closestx * math.sin(math.pi - self.periA) / r))
        else:
            a = self.Major - self.periD
            r = math.sqrt(a ** 2 + closestx ** 2 - 2 * a * closestx * math.cos(2 * math.pi - self.periA))
            self.Anglediff = math.pi - self.periA + (math.asin(closestx * math.sin(2 * math.pi - self.periA) / r))

        # position
        deltat = dayscalc(RefDay, Today)
        time = deltat / self.period * 2 * math.pi
        GM = 6.67e-11 * 1.989e30
        velocity = 0
        self.x = self.Major * math.cos(- self.periA + self.startA - self.Anglediff + time) * math.cos(self.periA) - \
                 self.Minor * math.sin(- self.periA + self.startA - self.Anglediff + time) * math.sin(self.periA) + self.cx
        self.y = self.Major * math.cos(- self.periA + self.startA - self.Anglediff + time) * math.sin(self.periA) + \
                 self.Minor * math.sin(- self.periA + self.startA - self.Anglediff + time) * math.cos(self.periA) + self.cy
        velocity = math.sqrt(GM * (2 / (math.sqrt(self.x ** 2 + self.y ** 2) * 1000) - 1 / (self.Major * 1000)))


with open('planetdata.json') as json_file:
    data = json.load(json_file)

fig = plt.gcf()
ax = fig.gca()

planets = []
for planet in data:
    body = Planet(float(data[planet]["Start Angle"]),
                  float(data[planet]["Perihelion Distance"]),
                  float(data[planet]["Perihelion Angle"]),
                  float(data[planet]["Period"]),
                  float(data[planet]["Eccentricity"]))
    plt.plot(body.ellipsex, body.ellipsey, color=data[planet]["Color"])
    bodySphere = plt.Circle((body.x, body.y), 10000000, color=data[planet]["Color"])
    ax.add_patch(bodySphere)
    planets.append(body)
sun = plt.Circle((0, 0), 10000000, color='y')
ax.add_patch(sun)
ax.set_aspect(1)
plt.show()






# Mercurius = Planet(0, 46001195.6, 1.351862225, 87.9691, 0.205630)
# Venus = Planet(0, 107477094, 2.296224977, 224.701, 0.006772)
# Aarde = Planet(0, 146605913, 1.796589572, 356.256, 0.016710219)
# Mars = Planet(0, 206744257.29, 5.874900435, 686.971, 0.0934)
# Jupiter = Planet(0, 740599219, 0.2501231351, 4332.59, 0.0489)
# Saturnus = Planet(0, 1352544268.6, 1.624151042, 10755.70, 0.0565)
# Uranus = Planet(0, 2735561623.4, 3.019506872, 30688.5, 0.04717)
# Neptunus = Planet(0, 4459512525.6, 0.8399222492, 60195, 0.008678)
# Pluto = Planet(0, 4436773649.2, 3.910846521, 90560, 0.2488)  # niet echt

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



