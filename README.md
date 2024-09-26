# Solar system simulator

Watch the positions of the planets and the moon in real time!

This program calculates the positions of all these objects relative to their star/planet.

My goal is to turn this into a background generator which creates a new up-to-date background for your computer.
## How to use
1. Make sure you have `pygame` and `requests` installed:
    ```
    pip install pygame
    pip install requests
    ```

2. Have a stable connection to the internet.
3. Run `main.py`

## Data

This makes use of the [Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html) to gather the data

## Roadmap
* Shadows on the planets/moon
* Turn image into a wallpaper (Windows)
* Use images for the planets instead of plain colors.
* Support for other operating systems/desktop manager (low priority)