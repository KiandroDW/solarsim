import re
import datetime

# Define the time span:
start_time = datetime.datetime.today().strftime('%Y-%m-%d-%H')
stop_time = (datetime.datetime.today() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d-%H')


def get_data(index, session):
    # Define API URL and SPK filename:
    url = ("https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='"
           f"{index}99"
           "'&OBJ_DATA='NO'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@10'&"
           f"START_TIME='{start_time}'&STOP_TIME='{stop_time}'&STEP_SIZE='1 d'&QUANTITIES='18,19'"
           )

    # Submit the API request:
    response = session.get(url)

    # Filter the needed data
    radius = re.search("Target radii .*: ([^,]*),", response.text).group(1)
    index1 = response.text.find("SOE")
    index2 = response.text.find("EOE")
    data = response.text[index1 + 4:index2 - 3]
    data = data.split()
    data = [element for i, element in enumerate(data) if i not in {3, 5}]
    data.append(radius)

    return data
