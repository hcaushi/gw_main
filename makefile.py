import urllib.request
import urllib.parse
import re
import time
import cx_Freeze
import sys

if sys.platform == "win32":
    base = "Win32GUI"

else:
    base = None

array = []

for i in range(1,10):
    array.append("level_0"+str(i)+".png")
    if i < 6:
        array.append("level_ex_0"+str(i)+".png")

array.append("level_10.png")

executables = [cx_Freeze.Executable("gw_main.py", base=base)]

cx_Freeze.setup(name = "Grid Wars",
                options = {"build_exe":
                                {"packages": ["tkinter","matplotlib", "pymysql", "pygame", "numpy", "PIL", "pickle", "matplotlib.pyplot", "PIL.Image", "PIL.ImageTk", "numpy.core._methods", "numpy.lib.format", ],
                                 "include_files": ["Grid Wars Title.png", "Basilisk.png", "Archer.png", "Chicken.png", "ChickenMan.png", "ChickenManMan.png", "Cleric.png", "Dragon.png", "Empty.png", "Goblin.png", "GoldenMan.png", "Griffin.png", "Grunt.png", "Knight.png", "Magician.png", "Peasant.png", "Phalanx.png", "SpearOrc.png", "Swordsman.png", "TreeMan.png"] + array
                                }
                           },
                version = "1.00",
                description = "Blah",
                executables = executables
                )
