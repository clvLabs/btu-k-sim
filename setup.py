from distutils.core import setup
import py2exe
import os

from src.config import Config

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FILES = [
  ('data', f'{THIS_PATH}/data/instruments.version'),
  ('data', f'{THIS_PATH}/data/instruments.zip'),
  ('data', f'{THIS_PATH}/data/scores.version'),
  ('data', f'{THIS_PATH}/data/scores.zip'),
]

setup(
  name=Config.App.name,
  version=Config.App.version,
  description="Asistente avanzado de batukación",
  requires=['pygame', 'pyyaml'],
  console=['sim.py'],
  data_files=DATA_FILES,
  )
