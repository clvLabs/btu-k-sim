import os
import sys
import glob
import pathlib
import shutil
import yaml
import urllib
import io
import requests
import zipfile
import pygame

from src.instrument import Instrument
from src.track import Track
from src.score import Score

class Config:

  class App:
    name = "btu-k-sim"
    version = "0.2"
    run_folder = ""
    data_folder = ""

  class AutoUpdate:
    update_link = ""
    @staticmethod
    def update_available():
      return Config.AutoUpdate.Instruments.update_available() or Config.AutoUpdate.Scores.update_available()

    class Instruments:
      @staticmethod
      def update_available():
        if not Config.AutoUpdate.Instruments.Version.remote:
          return False
        return Config.AutoUpdate.Instruments.Version.remote != Config.AutoUpdate.Instruments.Version.local

      class Version:
        local = ""
        remote = ""

    class Scores:
      @staticmethod
      def update_available():
        if not Config.AutoUpdate.Scores.Version.remote:
          return False
        return Config.AutoUpdate.Scores.Version.remote != Config.AutoUpdate.Scores.Version.local

      class Version:
        local = ""
        remote = ""


  class Simulator:
    instruments = {}
    scores = {}
    performance_scores = {}
    bpm = 100
    bpm_increment = 5
    metronome_instrument = "MT"
    director_instrument = "DD"
    metronome_track = None

    class Samples:
      items = {}


  class Display:
    width = 1900
    height = 1000
    background_color = "#000000"

    class HeaderText:

      line_height = 25

      class Font:
        name = "dejavusansmono"
        size = 20

      class Color:
        normal = "#FAFAFA"
        highlight = "#FF8822"
        title = "#00AA00"

    class ScoreText:

      line_height = 45

      class Font:
        name = "dejavusansmono"
        size = 40

      class Color:
        normal = "#FAFAFA"
        inactive = "#3C3C3C"
        done = "#777777"
        current = "#C80000"

    class Metronome:
      text = "1---2---3---4---"


    class Timeline:

      bar_hue = [170, 120, 60, 0]
      gradient = []

      class N16:
        width = 26
        height = 50
        margin_x = 2
        margin_y = 2

      class N4:
        width = 5
        height = 20
        color = (  0,   0,   0)

      class FirstN4:
        width = 10
        height = 20
        color = (  0,   0,   0)


  # -------------------------------------------
  # Config class initialization

  @staticmethod
  def _load_yaml():
    config_file = Config.App.run_folder / "config.yml"
    print(f"- Leyendo archivo de configuración [{config_file}]")

    if not os.path.isfile(config_file):
      print("  - El archivo no existe, generando configuración por defecto")
      Config._write_yaml()

    with open(config_file) as f:
      yml = yaml.load(f, Loader=yaml.SafeLoader)

      Config.AutoUpdate.update_link = yml['auto_update']['update_link']

      Config.Simulator.bpm = yml['simulator']['default_bpm']
      Config.Simulator.bpm_increment = yml['simulator']['bpm_increment']


  @staticmethod
  def _write_yaml():
    config_file = Config.App.run_folder / "config.yml"
    print(f"- Escribiendo archivo de configuración [{config_file}]")

    data = {
      "auto_update": {},
      "simulator": {},
    }

    data['auto_update']['update_link'] = Config.AutoUpdate.update_link

    data['simulator']['default_bpm'] = Config.Simulator.bpm
    data['simulator']['bpm_increment'] = Config.Simulator.bpm_increment

    with open(config_file, "w") as f:
      f.write(yaml.dump(data))


  @staticmethod
  def _load_instruments():
    instruments_file = Config.App.data_folder / "instruments/instruments.yml"
    print(f"- Cargando configuración de instrumentos [{instruments_file}]")

    if not os.path.isfile(instruments_file):
      print(f"ERROR: No se puede abrir {instruments_file}")
      sys.exit(1)

    with open(instruments_file) as f:
      yml = yaml.load(f, Loader=yaml.SafeLoader)

      for (id, data) in yml['instruments'].items():
        Config.Simulator.instruments[id] = Instrument(
          id,
          data['name'],
          data['samples']
        )


  @staticmethod
  def _load_scores():
    scores_pattern = str(Config.App.data_folder / "scores/*.yml")
    score_list = glob.glob(scores_pattern)

    print(f"- Abriendo partituras yml")

    for score_file in sorted(score_list):
      try:
        print(f"  - Abriendo [{score_file}]")
        with open(score_file) as f:
          yml = yaml.load(f, Loader=yaml.SafeLoader)
          name = yml['name']
          sections = yml['sections']

          _score = Score(Config, name, sections)
          Config.Simulator.scores[name] = _score

          perf_name = f"*{name}*"
          print(f"    - Creando versión \"de bolo\" [{perf_name}]")
          Config.Simulator.performance_scores[perf_name] = Score.create_performance_version(Config, _score, perf_name)

      except Exception as e:
        print(f"ERROR cargando partitura [{score_file}]: {e}")


  @staticmethod
  def _load_samples():
    print(f"- Abriendo samples de instrumentos")
    for score in Config.Simulator.scores.values():
      for section in score.sections.values():
        for track in section.tracks.values():
          Config._load_track_samples(track)


  @staticmethod
  def _load_track_samples(track):
    for (note, sample) in track.instrument.samples.items():
      if type(sample) is pygame.mixer.Sound:
        continue
      if sample not in Config.Simulator.Samples.items:
        sample_path = Config.App.data_folder / f"instruments/samples/{sample}"
        print(f"  - Sample [{sample_path}]")
        try:
          Config.Simulator.Samples.items[sample] = pygame.mixer.Sound(sample_path)
        except Exception as e:
          print(f"AVISO: no se pudo cargar {sample_path} ({e})")

      track.instrument.samples[note] = Config.Simulator.Samples.items[sample]


  @staticmethod
  def _create_metronome_track():
    print(f"- Creando pista de metrónomo")
    _notes = "X   -   -   -   " * 64
    Config.Simulator.metronome_track = Track(Config, Config.Simulator.metronome_instrument, _notes)
    Config.Simulator.metronome_track.channel = pygame.mixer.Channel(0)
    Config._load_track_samples(Config.Simulator.metronome_track)


  @staticmethod
  def _create_gradients():
    print(f"- Creando degradados de color")
    for _bar in range(4):
      _h = Config.Display.Timeline.bar_hue[_bar]
      _s = 0
      _v = 100
      _a = 100
      for _n4 in range(4):
        _s += 25
        _v -= 10
        for _n16 in range(4):
          _hsva = (_h, _s, _v, _a)
          Config.Display.Timeline.gradient.append(_hsva)


  @staticmethod
  def _check_resource_folders():
    print(f"- Comprobando carpetas de recursos")

    def _extract_zip(resource_type):
      _folder = Config.App.data_folder / resource_type
      _zip = Config.App.data_folder / f"{resource_type}.zip"
      if not os.path.isdir(_folder):
        print(f"AVISO: {_folder} no existe, descomprimiendo .ZIP...")

        if not os.path.isfile(_zip):
          print(f"ERROR: No existe [{_zip}]")
          print(f"Intentando descargar actualizaciones")
          if not Config.apply_resource_updates():
            sys.exit(1)
          # Already downloaded last resources, don't need to extract anything more...
          return

        try:
          with zipfile.ZipFile(_zip, 'r') as z:
            z.extractall(Config.App.data_folder)
        except Exception as e:
          print(f"ERROR descomprimiendo [{_zip}]: {e}")
          sys.exit(1)

    _extract_zip("instruments")
    _extract_zip("scores")


  @staticmethod
  def _check_resource_updates():
    print(f"- Comprobando actualizaciones de recursos")

    def _get_local_version(resource_type):
      _version_file = Config.App.data_folder / f"{resource_type}.version"
      try:
        with open(_version_file) as f:
          version = f.read().replace('\n','').strip()
      except Exception as e:
        print(f"AVISO: no se pudo cargar {_version_file} ({e})")
        version = ""
      return version

    def _get_remote_version(resource_type):
      url = f"{Config.AutoUpdate.update_link}/{resource_type}.version"
      try:
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
          version = req.text.replace('\n','').strip()
        else:
          raise Exception(f"Error HTTP {req.status_code}")
      except Exception as e:
        print(f"AVISO: no se pudo cargar {url} ({e})")
        version = ""
      return version

    Config.AutoUpdate.Instruments.Version.local = _get_local_version("instruments")
    Config.AutoUpdate.Scores.Version.local = _get_local_version("scores")

    Config.AutoUpdate.Instruments.Version.remote = _get_remote_version("instruments")
    Config.AutoUpdate.Scores.Version.remote = _get_remote_version("scores")


    print(f"  - Instrumentos:")
    print(f"    - Versión local:  {Config.AutoUpdate.Instruments.Version.local}")
    print(f"    - Última versión: {Config.AutoUpdate.Instruments.Version.remote}")
    if Config.AutoUpdate.Instruments.update_available():
      print(f"    - ACTUALIZACIÓN DISPONIBLE!")

    print(f"  - Partituras:")
    print(f"    - Versión local:  {Config.AutoUpdate.Scores.Version.local}")
    print(f"    - Última versión: {Config.AutoUpdate.Scores.Version.remote}")
    if Config.AutoUpdate.Scores.update_available():
      print(f"    - ACTUALIZACIÓN DISPONIBLE!")


  @staticmethod
  def apply_resource_updates():
    print(f"- Descargando actualizaciones de recursos")

    if not Config.AutoUpdate.update_available():
      print(f"  - No hay actualizaciones disponibles")
      return False


    def _update_resource(resource_type):
      url = f"{Config.AutoUpdate.update_link}/{resource_type}.zip"
      folder = Config.App.data_folder / resource_type
      zip_path = Config.App.data_folder / f"{resource_type}.zip"
      try:
        print(f"    - Descargando {url}")
        http_response = urllib.request.urlopen(url)
        if http_response.status != requests.codes.ok:
          raise Exception(f"Error HTTP {http_response.status}")

        print(f"    - Eliminando recursos antiguos")
        try:
          if os.path.isdir(folder):
            shutil.rmtree(folder)
          if os.path.isfile(zip_path):
            os.remove(zip_path)
        except Exception as e:
          print(f"AVISO: error eliminando recursos ({e})")

        print(f"    - Descomprimiendo nuevos recursos")
        zip_bytes = io.BytesIO(http_response.read())
        z = zipfile.ZipFile(zip_bytes)
        z.extractall(Config.App.data_folder)
        print(f"    - Grabando archivo .zip")
        with open(zip_path, "wb") as f:
          f.write(zip_bytes.getbuffer())
      except Exception as e:
        print(f"AVISO: no se pudo cargar {url} ({e})")
        return False
      return True


    def _update_local_version(resource_type, version):
      _version_file = Config.App.data_folder / f"{resource_type}.version"
      try:
        with open(_version_file, "w") as f:
          f.write(version)
      except Exception as e:
        print(f"AVISO: no se pudo actualizar {_version_file} ({e})")
        return False
      return True


    updates_applied = False

    if Config.AutoUpdate.Instruments.update_available():
      print(f"  - Descargando nuevos instrumentos")
      if _update_resource("instruments"):
        if _update_local_version("instruments", Config.AutoUpdate.Instruments.Version.remote):
          Config.AutoUpdate.Instruments.Version.local = Config.AutoUpdate.Instruments.Version.remote
          print(f"  - Instrumentos actualizados. Versión: {Config.AutoUpdate.Instruments.Version.local}")
          updates_applied = True

    if Config.AutoUpdate.Scores.update_available():
      print(f"  - Descargando nuevas partituras")
      if _update_resource("scores"):
        if _update_local_version("scores", Config.AutoUpdate.Scores.Version.remote):
          Config.AutoUpdate.Scores.Version.local = Config.AutoUpdate.Scores.Version.remote
          print(f"  - Partituras actualizadas. Versión: {Config.AutoUpdate.Scores.Version.local}")
          updates_applied = True

    return updates_applied


  @staticmethod
  def init():
    print("- Inicializando configuración")
    if os.name == "nt":
      Config.App.run_folder = pathlib.Path(os.getcwd())
    else:
      Config.App.run_folder = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent

    Config.App.data_folder = Config.App.run_folder / "data"

    print(f"  - Ejecutando desde: {Config.App.run_folder}")
    print(f"  - Carpeta de datos: {Config.App.data_folder}")

    # Overwrite configuration values from yaml file
    Config._load_yaml()

    # Check for available resource updates
    Config._check_resource_updates()

    # Check if data folders do not exist yet (first run)
    Config._check_resource_folders()

    # Read instruments/scores/samples
    Config._load_instruments()
    Config._load_scores()
    Config._load_samples()

    # Create metronome track
    Config._create_metronome_track()

    # Create timeline gradients from bar hue list
    Config._create_gradients()
