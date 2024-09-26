# Solar system simulated background

Watch the positions of the planets and the moon in real time!

This program calculates the positions of all these objects relative to their star/planet.  
When doing all the steps, a new image will be generated everytime you log in to Windows.
## How to use
1. Have python3 installed, you can test this by using the  `python3` command in the Command Prompt
2. Make sure you have `pygame`, `requests` and `pillow` installed via Command Prompt:
    ```
    > pip install pygame
    > pip install requests
    > pip install pillow
    ```

3. Run the [setup script](python_scripts/setup.py). This will make sure your background will automatically change on startup.
4. (optional) Run [main.pyw](python_scripts/main.pyw) to generate a first background.

### Run scripts
If you have python3 installed and all the packages, you can run a script by running:
```
> python3 path_to_file
```
To get path_to_file, you can right-click the file in File Explorer -> Copy as Path which will save it to your clipboard.

## Data

This makes use of the [Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html) to gather the data

## Roadmap
* Shadows on the planets/moon
* Use images for the planets instead of plain colors.
* Support for other operating systems/desktop manager (low priority)