from distutils.core import setup
import os
import pathlib
import py2exe

from src.config import Config

THIS_PATH = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
DATA_FILES = [
  ('data', [
    str(THIS_PATH / 'data/instruments.version'),
    str(THIS_PATH / 'data/instruments.zip'),
    str(THIS_PATH / 'data/scores.version'),
    str(THIS_PATH / 'data/scores.zip'),
  ])
]

setup(
  name=Config.App.name,
  version=Config.App.version,
  description="Asistente avanzado de batukación",
  requires=['pygame', 'pyyaml'],
  console=['btu-k-sim.py'],
  data_files=DATA_FILES,
  )
