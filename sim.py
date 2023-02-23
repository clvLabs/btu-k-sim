#!/usr/bin/python3
from os.path import dirname, abspath
import argparse
from src.config import Config
from src.simulator import Simulator

Config.App.run_folder = dirname(abspath(__file__))

print(f"{Config.App.name} v{Config.App.version}")

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--play', help='Automatically start playing.', action='store_true', default=False)
args = parser.parse_args()

sim = Simulator(Config)

if args.play:
  sim.playing = True

sim.run()

print("Hasta la próxima!")
