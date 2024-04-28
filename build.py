# File for installing dependencies and building to executable.
import os
import time

print("WARNING: This program assumes you have pip and tkinter installed.")

print("Waiting 3 seconds to start.")
time.sleep(3)

print("Installing base modules for build: pygame, raylib, tripy, numpy, pyinstaller")
os.system("pip install pygame")
os.system("pip install raylib")
os.system("pip install tripy")
os.system("pip install numpy")
os.system("pip install pyinstaller")

print("Finished installing dependencies. Building to executable.")

print("Waiting 3 seconds to start.")
time.sleep(3)

os.system("pyinstaller main.py --distpath . -F -n TitanGameEngine --add-data projects.json:. --add-data assets:.")