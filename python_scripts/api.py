import re
import datetime

# stop_time = today:
stop_time = datetime.datetime.today()


# If you want a specific day instead of the current day use:
# stop_time = datetime.datetime(year=2000, month=1, day=1)


def get_path(index: int, body_type: str, time_jump: int):
    start_time = stop_time - datetime.timedelta(hours=(time_jump * 99))
    planet_path = ("/api/horizons.api?format=text&"
                   f"COMMAND=%27{index}99%27&"
                   "OBJ_DATA=%27NO%27&MAKE_EPHEM=%27YES%27&EPHEM_TYPE=%27OBSERVER%27&CENTER=%27500@10%27&"
                   f"START_TIME=%27{start_time.strftime('%Y-%m-%d-%H')}%27&"
                   f"STOP_TIME=%27{stop_time.strftime('%Y-%m-%d-%H')}%27&"
                   f"STEP_SIZE=%27{time_jump}%20h%27&QUANTITIES=%2718,19%27")

    moon_path = ("/api/horizons.api?format=text&"
                 "COMMAND=%27301%27&"
                 "OBJ_DATA=%27NO%27&MAKE_EPHEM=%27YES%27&EPHEM_TYPE=%27OBSERVER%27&CENTER=%27500@399%27&"
                 f"START_TIME=%27{start_time.strftime('%Y-%m-%d-%H')}%27&"
                 f"STOP_TIME=%27{stop_time.strftime('%Y-%m-%d-%H')}%27&"
                 f"STEP_SIZE=%27{time_jump}%20h%27&QUANTITIES=%2731,20%27")

    return planet_path if body_type == 'PLANET' else moon_path


def get_data(response) -> tuple[list[list[float]], float]:
    # Filter the needed data
    radius = re.search("Target radii .*: ([^,]*),", response).group(1)
    index1 = response.find("SOE")
    index2 = response.find("EOE")
    data = response[index1 + 4:index2 - 3]
    data = data.split("\n")
    data = [element.split() for element in data]
    data = [[float(element[2]), float(element[4])] for element in data]

    return data, float(radius)
