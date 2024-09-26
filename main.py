import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import json

import requests

import api
import planet
import screen

# Open the json file with all the date of the planets
with open("innerplanetdata.json") as json_file:
    data_inner = json.load(json_file)

with open("outerplanetdata.json") as json_file:
    data_outer = json.load(json_file)

# Load all the planets
try:
    with requests.Session() as s:
        for p in data_inner:
            api_data = api.get_data(data_inner[p]["Index"], "PLANET", s)
            planet.Planet(api_data[2], api_data[3], api_data[4], data_inner[p]["Color"], 3.5, 3, 2, 4)
        for p in data_outer:
            api_data = api.get_data(data_outer[p]["Index"], "PLANET", s)
            planet.Planet(api_data[2], api_data[3], api_data[4], data_outer[p]["Color"], 124, 6/5, 4, 0.25)
except requests.exceptions.ConnectionError:
    exit(0)

# Start the screen
screen.start(planet.planets)
