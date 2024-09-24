import datetime
import json
import math
import pygame
import sys
import planet

# You can change these settings inside the simulation
# The filename of the JSON file with planet-data
filename = "innerplanetdata.json"
# RefDay: (year, month, date, hour) is the time on which the simulation is based. If you change it,
# change the Start Angle in the JSON file to the correct angle on that date if you want it to be accurate
RefDay = datetime.datetime(2023, 3, 20, 22)
# These 4 are the only things you should change to not brake it

Today = datetime.datetime(datetime.datetime.today().year,
                          datetime.datetime.today().month,
                          datetime.datetime.today().day,
                          datetime.datetime.today().hour)


# Open the json file with all the date of the planets
with open(filename) as json_file:
    data = json.load(json_file)

# Call the planet class on all the planets
planets = planet.planets
for p in data:
    planet.Planet(data[p]["Name"],
                  float(data[p]["Start Angle"]),
                  float(data[p]["Perihelion Distance"]),
                  float(data[p]["Perihelion Angle"]),
                  float(data[p]["Period"]),
                  float(data[p]["Eccentricity"]),
                  float(data[p]["Radius"]),
                  data[p]["Color"],
                  )

# Draw the image repeatedly.
while True:
    planet.screen.fill((0, 0, 0))
    # Close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print(f'Refday = {RefDay}')
            for p in planets:
                print(f'Start Angle {p.name} = {(p.startA + p.totalw) % (2 * math.pi)}')
            sys.exit()

    # Draw the sun and every planet
    for p in planets:
        p.process()
        pygame.draw.circle(planet.screen, [255, 242, 222], (int(planet.windowdim[0]) / 2, int(planet.windowdim[1]) / 2),
                           radius=p.solarradius)
    modechanging = False

    # Makes the movement fast until the planets are at their current positions
    if RefDay < Today:
        fps = 120
        RefDay = RefDay + datetime.timedelta(minutes=60)
    else:
        fps = 10
        spf = 0.1
        RefDay = RefDay + datetime.timedelta(seconds=1)

    pygame.display.flip()
    planet.fpsClock.tick(fps)
