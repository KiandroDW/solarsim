import re
import datetime

import requests

# stop_time = today:
stop_time = datetime.datetime.today()

# If you want a specific day instead of the current day use:
# stop_time = datetime.datetime(year=2000, month=1, day=1)


def get_data(index: int, body_type: str, time_jump: int, session: requests.Session
             ) -> tuple[list[list[float]], float]:
    start_time = stop_time - datetime.timedelta(hours=(time_jump * 99))
    # Define API URL:
    planet_url = ("https://ssd.jpl.nasa.gov/api/horizons.api?format=text&"
                  f"COMMAND='{index}99'&OBJ_DATA='NO'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@10'&"
                  f"START_TIME='{start_time.strftime('%Y-%m-%d-%H')}'&"
                  f"STOP_TIME='{stop_time.strftime('%Y-%m-%d-%H')}'&"
                  f"STEP_SIZE='{time_jump} h'&QUANTITIES='18,19'"
                  )

    moon_url = ("https://ssd.jpl.nasa.gov/api/horizons.api?format=text&"
                "COMMAND='301&OBJ_DATA='NO'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&"
                f"START_TIME='{start_time.strftime('%Y-%m-%d-%H')}'&"
                f"STOP_TIME='{stop_time.strftime('%Y-%m-%d-%H')}'&"
                f"STEP_SIZE='{time_jump} h'&QUANTITIES='31,20'"
                )

    # Submit the API request:
    response = session.get(planet_url if body_type == "PLANET" else moon_url)

    # Filter the needed data
    radius = re.search("Target radii .*: ([^,]*),", response.text).group(1)
    index1 = response.text.find("SOE")
    index2 = response.text.find("EOE")
    data = response.text[index1 + 4:index2 - 3]
    data = data.split("\n")
    data = [element.split() for element in data]
    data = [[float(element[2]), float(element[4])] for element in data]

    return data, float(radius)
