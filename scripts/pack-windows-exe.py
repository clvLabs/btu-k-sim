#!/usr/bin/python3
import os
import sys
import pathlib
import shutil

print("***")
print("*** Cleaning previous build files")
print("***")

for f in ["btu-k-sim.spec"]:
  if os.path.isfile(f):
    os.remove(f)

for f in ["build", "dist", "pack-tmp"]:
  if os.path.isdir(f):
    shutil.rmtree(f)

print("***")
print("*** Building btu-k-sim.exe")
print("***")

os.system("pyinstaller btu-k-sim.py --onefile")

if not os.path.isfile("dist/btu-k-sim.exe"):
  print("ERROR: Resulting executable not found")
  sys.exit(1)

print("***")
print("*** Gathering executable and resources")
print("***")

temp_folder = pathlib.Path(os.getcwd() + "/pack-tmp")
program_folder = temp_folder / "btu-k-sim"
data_folder = temp_folder / "btu-k-sim/data"
os.mkdir(temp_folder)
os.mkdir(program_folder)
os.mkdir(data_folder )

shutil.copy("dist/btu-k-sim.exe", program_folder)
shutil.copy("config.yml", program_folder)

shutil.copy("data/instruments.version", data_folder)
shutil.copy("data/instruments.zip", data_folder)

shutil.copy("data/scores.version", data_folder)
shutil.copy("data/scores.zip", data_folder)

print("***")
print("*** Creating dist/btu-k-sim.zip")
print("***")

shutil.make_archive("dist/btu-k-sim", 'zip', temp_folder)

print("***")
print("*** Cleaning up")
print("***")

shutil.rmtree(temp_folder)

print("***")
print("*** FINISHED")
print("***")

