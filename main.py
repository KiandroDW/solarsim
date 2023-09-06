import math
import matplotlib.pyplot as plt


class Planet:
    """
    StartAngle: The angle between the vernal equinox and the position of the planet in radians at T=0.

    PerihelionDistance: The distance from the star in the planet's perihelion in kilometers.

    perihelionAngle: The angle between the vernal equinox and the perihelion of the planet in radians.

    period: The period of the planet in days.

    eccentricity: how eccentric the ellips is with 0 < eccentricity < 1.

    This calculates all elements of the orbit.
    """
    def __init__(self, StartCoordinates: float, PerihelionDistance: float,
                  PerihelionAngle: float, period: float, eccentricity: float):
        self.startC = StartCoordinates
        self.periD = PerihelionDistance
        self.periA = PerihelionAngle
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
        cx = self.Major * math.cos(self.periA) - periC[0]
        cy = self.Major * math.sin(self.periA) - periC[1]
        while t < 6.3:
            x.append(self.Major * math.cos(t) * math.cos(self.periA) - self.Minor * math.sin(t) * math.sin(self.periA) + cx)
            y.append(self.Major * math.cos(t) * math.sin(self.periA) + self.Minor * math.sin(t) * math.cos(self.periA) + cy)
            t += 0.1
        self.x, self.y = x, y


Mercurius = Planet(0, 46001195.6, 1.351862225, 87.9691, 0.205630)
Venus = Planet(0, 107477094, 2.296224977, 224.701, 0.006772)
Aarde = Planet(0, 146605913, 1.796589572, 356.25, 0.016710219)
Mars = Planet(0, 206744257.29, 5.874900435, 686.971, 0.0934)
Jupiter = Planet(0, 740599219, 0.2501231351, 4332.59, 0.0489)
Saturnus = Planet(0, 1352544268.6, 1.624151042, 10755.70, 0.0565)
Uranus = Planet(0, 2735561623.4, 3.019506872, 30688.5, 0.04717)
Neptunus = Planet(0, 4459512525.6, 0.8399222492, 60195, 0.008678)
Pluto = Planet(0, 4436773649.2, 3.910846521, 90560, 0.2488)  # niet echt

plt.plot(Mercurius.x, Mercurius.y, color='k')
plt.plot(Venus.x, Venus.y, color='y')
plt.plot(Aarde.x, Aarde.y, color='b')
plt.plot(Mars.x, Mars.y, color='r')
plt.plot(Jupiter.x, Jupiter.y, color='y')
plt.plot(Saturnus.x, Saturnus.y, color='y')
plt.plot(Uranus.x, Uranus.y, color='c')
plt.plot(Neptunus.x, Neptunus.y, color='b')
plt.plot(Pluto.x, Pluto.y, color='k')
plt.show()
