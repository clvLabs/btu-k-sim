#!/usr/bin/python3
import argparse
import importlib
import src.config
import src.simulator

print(f"{src.config.Config.App.name} v{src.config.Config.App.version}")

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--play', help='Automatically start playing.', action='store_true', default=False)
parser.add_argument('-j', '--jam', help='Automatically start jam mode.', action='store_true', default=False)
args = parser.parse_args()

finished = False

while not finished:
  sim = src.simulator.Simulator(src.config.Config)

  if args.play:
    sim.playing = True

  if args.jam:
    sim.jam_mode = True

  sim.run()

  if sim.need_update_restart:
    print("- Reiniciando simulador")
    importlib.reload(src.config)
  else:
    finished = True

print("Hasta la próxima!")
