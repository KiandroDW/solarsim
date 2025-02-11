import getpass
import os
from pathlib import Path
from exceptions import FileSolarSimException

USER_NAME = getpass.getuser()

home = Path.home()
path = str(home) + "/SolarSimBackground"
if not os.path.exists(path):
    os.mkdir(path)

file_path = os.path.dirname(os.path.realpath(__file__)) + "\\main.pyw"
vbs_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME

try:
    files = os.listdir(vbs_path)
    for file in files:
        vbs_file_path = os.path.join(path, file)
        if os.path.isfile(vbs_file_path):
            os.remove(vbs_file_path)
except OSError:
    raise FileSolarSimException()

with open(vbs_path + '\\' + "run.vbs", "w+") as vbs_file:
    vbs_file.write('Set objShell = CreateObject("WScript.Shell")\n')
    vbs_file.write('objShell.Run "pythonw %s", 0, False' % file_path)
