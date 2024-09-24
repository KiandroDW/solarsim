import math
import screen

# Define the different scales for the mode
scale = 600000
rscale = 200


class Orbit:
    def __init__(self, start_angle: float, perihelion_distance: float,
                 perihelion_angle: float, period: float, eccentricity: float):
        self.start_angle = start_angle
        self.peri_d = perihelion_distance
        self.peri_a = perihelion_angle
        self.period = period
        self.ecc = eccentricity

        self.semi_major_axis = self.peri_d / (1 - self.ecc)
        self.semi_minor_axis = math.sqrt(-(self.ecc ** 2 - 1) * self.semi_major_axis ** 2)

        self.cx = self.semi_major_axis * math.cos(self.peri_a) - self.peri_d * math.cos(self.peri_a)
        self.cy = self.semi_major_axis * math.sin(self.peri_a) - self.peri_d * math.sin(self.peri_a)

        t = 0
        x, y = [], []
        while t < 2 * math.pi:
            x.append(self.semi_major_axis * math.cos(t) * math.cos(self.peri_a) -
                     self.semi_minor_axis * math.sin(t) * math.sin(self.peri_a) - self.cx)
            y.append(self.semi_major_axis * math.cos(t) * math.sin(self.peri_a) +
                     self.semi_minor_axis * math.sin(t) * math.cos(self.peri_a) - self.cy)
            t += 0.01

        self.orbit_list = []
        for pos in range(len(x)):
            self.orbit_list.append((x[pos] / scale + int(screen.window_dim[0]) / 2, y[pos] / scale + int(screen.window_dim[1]) / 2))

        closesty = min([math.fabs(j) for j in y])
        closesty = - closesty if closesty not in y else closesty
        place = y.index(closesty)
        if x[place] < 0:
            y.remove(closesty)
            closesty2 = min([math.fabs(j) for j in y])
            closesty2 = - closesty2 if closesty2 not in y else closesty2
            place = y.index(closesty2)
        closestx = x[place]

        # Use this x-coordinate to find the angle from the center at which the planet is at that position
        if math.pi / 2 < perihelion_angle < 3 * math.pi / 2:
            a = self.semi_major_axis - self.peri_d
            r = math.sqrt(a ** 2 + closestx ** 2 - 2 * a * closestx * math.cos(math.pi - self.peri_a))
            self.angle_diff = self.peri_a - (math.asin(closestx * math.sin(math.pi - self.peri_a) / r))
        else:
            a = self.semi_major_axis - self.peri_d
            r = math.sqrt(a ** 2 + closestx ** 2 - 2 * a * closestx * math.cos(2 * math.pi - self.peri_a))
            self.angle_diff = math.pi - self.peri_a + (math.asin(closestx * math.sin(2 * math.pi - self.peri_a) / r))

        # Calculate the position of the planet at the start
        self.x = self.semi_major_axis * math.cos(- self.peri_a - self.start_angle + self.angle_diff) * math.cos(self.peri_a) - \
                 self.semi_minor_axis * math.sin(- self.peri_a - self.start_angle + self.angle_diff) * math.sin(self.peri_a) - self.cx
        self.y = self.semi_major_axis * math.cos(- self.peri_a - self.start_angle + self.angle_diff) * math.sin(self.peri_a) + \
                 self.semi_minor_axis * math.sin(- self.peri_a - self.start_angle + self.angle_diff) * math.cos(self.peri_a) - self.cy

        self.position = [self.x / scale + int(screen.window_dim[0]) / 2, self.y / scale + int(screen.window_dim[1]) / 2]
        self.outerposition = [0, 0]
        self.totalw = 0
