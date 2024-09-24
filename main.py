import datetime
import json
import planet
import screen

# You can change these settings inside the simulation
# The filename of the JSON file with planet-data
filename = "innerplanetdata.json"
# RefDay: (year, month, date, hour) is the time on which the simulation is based. If you change it,
# change the Start Angle in the JSON file to the correct angle on that date if you want it to be accurate
ref_day = datetime.datetime(2023, 3, 20, 22)
# These are the only things you should change to not brake the program


# Open the json file with all the date of the planets
with open(filename) as json_file:
    data = json.load(json_file)

# Load all the planets
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

# Start the screen
screen.start(ref_day, planet.planets)
