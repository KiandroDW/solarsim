import getpass
import os
from pathlib import Path
from exceptions import FileSolarSimException

# Change this to True if you want a terminal to pop up when loading the background.
verbose = False

USER_NAME = getpass.getuser()

home = Path.home()
path = str(home) + "/SolarSimBackground"
if not os.path.exists(path):
    os.mkdir(path)

file_path = os.path.dirname(os.path.realpath(__file__)) + "\\main.pyw"
vbs_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME

try:
    for file in ["run.bat", "run.vbs"]:
        search_path = os.path.join(vbs_path, file)
        if os.path.exists(search_path):
            os.remove(search_path)
except OSError:
    raise FileSolarSimException()

if not verbose:
    with open(vbs_path + '\\' + "run.vbs", "w+") as vbs_file:
        vbs_file.write('Set objShell = CreateObject("WScript.Shell")\n')
        vbs_file.write('objShell.Run "pythonw %s", 0, False' % file_path)
else:
    with open(vbs_path + '\\' + "run.bat", "w+") as bat_file:
        bat_file.write("python %s" % file_path)
