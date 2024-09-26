import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import json

import requests

import api
import planet
import screen
from time import sleep

# Open the json file with all the date of the planets
with open("innerplanetdata.json") as json_file:
    data_inner = json.load(json_file)

with open("outerplanetdata.json") as json_file:
    data_outer = json.load(json_file)

with open("moondata.json") as json_file:
    data_moon = json.load(json_file)

# Load all the planets
passed = False
counter = 0
while not passed:
    try:
        with requests.Session() as s:
            for p in data_inner:
                api_data = api.get_data(data_inner[p]["Index"], "PLANET", s)
                planet.Planet(api_data[2], api_data[3], api_data[4], data_inner[p]["Color"], 3.5, 3, 2, 4)
            for p in data_outer:
                api_data = api.get_data(data_outer[p]["Index"], "PLANET", s)
                planet.Planet(api_data[2], api_data[3], api_data[4], data_outer[p]["Color"], 124, 6/5, 4, 0.25)
            for m in data_moon:
                api_data = api.get_data(-1, "MOON", s)
                planet.Planet(api_data[2], api_data[3], api_data[4], data_moon[m]["Color"], 0.012, 6/5, 4/3, 4)
        passed = True
    except requests.exceptions.ConnectionError:
        if counter == 10:
            exit(0)
        counter += 1
        sleep(10)
        pass

# Start the screen
screen.start(planet.planets)
