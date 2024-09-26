import getpass
import os
from pathlib import Path
USER_NAME = getpass.getuser()

home = Path.home()
path = str(home) + "/SolarSimBackground"
if not os.path.exists(path):
    os.mkdir(path)

file_path = os.path.dirname(os.path.realpath(__file__)) + "\\main.pyw"
bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME

try:
    files = os.listdir(bat_path)
    for file in files:
        bat_file_path = os.path.join(path, file)
        if os.path.isfile(bat_file_path):
            os.remove(bat_file_path)
except OSError:
    print("Error occurred while deleting files.")
    exit(1)


with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
    bat_file.write(r'python3 "%s"' % file_path)
