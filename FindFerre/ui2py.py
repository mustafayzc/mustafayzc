import subprocess
import sys

command = f"python3 -m PyQt5.uic.pyuic findferre.ui -o findferreUI2.py -x"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
command2 = f"python3 -m PyQt5.pyrcc_main ass.qrc -o ass_rc.py"
result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)
print("bitti amk")

