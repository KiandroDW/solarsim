import json
import requests
import api
from time import sleep
import os
# make pygame not print support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import body
import screen

# Open the json files with all the data of the bodies
with open(os.path.dirname(os.path.realpath(__file__)).replace("python_scripts", "json_files") + "\\innerplanetdata.json") as json_file:
    data_inner = json.load(json_file)

with open(os.path.dirname(os.path.realpath(__file__)).replace("python_scripts", "json_files") + "\\outerplanetdata.json") as json_file:
    data_outer = json.load(json_file)

with open(os.path.dirname(os.path.realpath(__file__)).replace("python_scripts", "json_files") + "\\moondata.json") as json_file:
    data_moon = json.load(json_file)

# Load all the bodies
# The program can only work when you have internet connection, so when there's none the program will wait for max 100s
# before closing.
passed = False
counter = 0
while not passed:
    try:
        with requests.Session() as s:
            for p in data_inner:
                api_data = api.get_data(data_inner[p]["Index"], "PLANET", 6, s)
                body.Body(api_data[0], api_data[1], data_inner[p]["Color"], 3.5, 3, 2, 250)
            for p in data_outer:
                api_data = api.get_data(data_outer[p]["Index"], "PLANET", 672, s)
                body.Body(api_data[0], api_data[1], data_outer[p]["Color"], 124, 6 / 5, 4, 4000)
            for m in data_moon:
                api_data = api.get_data(-1, "MOON", 1, s)
                body.Body(api_data[0], api_data[1], data_moon[m]["Color"], 0.015, 6 / 5, 4 / 3, 125)
        passed = True
    except requests.exceptions.ConnectionError:
        if counter == 10:
            exit(1)
        counter += 1
        # Only try connecting once every 10 seconds
        sleep(10)
        pass

# Start the screen
screen.start(body.bodies)
