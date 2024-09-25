import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import json

import requests

import api
import planet
import screen

# You can change these settings inside the simulation
# The filename of the JSON file with planet-data
filename = "innerplanetdata.json"


# Open the json file with all the date of the planets
with open(filename) as json_file:
    data = json.load(json_file)

# Load all the planets
try:
    with requests.Session() as s:
        for p in data:
            planet2.Planet2(*api.get_data(data[p]["Index"], s), color=data[p]["Color"])
except requests.exceptions.ConnectionError:
    exit(0)

# Start the screen
screen.start(planet2.planets)
