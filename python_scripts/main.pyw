import json
import socket
import api
from time import sleep
import os
import threading
import dugong
import ssl
import time
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
        t0 = time.time()
        paths = []
        for p in data_inner:
            paths.append(api.get_path(data_inner[p]["Index"], "PLANET", 6))

        for p in data_outer:
            paths.append(api.get_path(data_outer[p]["Index"], "PLANET", 672))

        for m in data_moon:
            paths.append(api.get_path(-1, "MOON", 1))

        with dugong.HTTPConnection("ssd.jpl.nasa.gov", port=dugong.HTTPS_PORT, ssl_context=ssl.create_default_context()) as connection:
            def send_requests():
                for body_path in paths:
                    connection.send_request("GET", body_path)

            thread = threading.Thread(target=send_requests)
            thread.run()
            responses = []
            for path in paths:
                resp = connection.read_response()
                assert resp.status == 200
                responses.append(connection.readall().decode("utf-8"))

        for response in responses:
            api_data = api.get_data(response)
            body.Body(api_data[0], api_data[1], data_inner["Earth"]["Color"], 3.5, 3, 2, 250)
        print(time.time() - t0)
        exit(0)


        passed = True
        # body.Body(api_data[0], api_data[1], data_inner[p]["Color"], 3.5, 3, 2, 250)
        # body.Body(api_data[0], api_data[1], data_outer[p]["Color"], 124, 6 / 5, 4, 4000)
        #  body.Body(api_data[0], api_data[1], data_moon[m]["Color"], 0.015, 6 / 5, 4 / 3, 125)
    except socket.gaierror:
        if counter == 10:
            exit(1)
        counter += 1
        # Only try connecting once every 10 seconds
        sleep(10)
        pass

# Start the screen
screen.start(body.bodies)

