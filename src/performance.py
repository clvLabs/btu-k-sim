import math
import re
import copy

INTRO_KEY = "intro"
END_KEY = "fin"
BASE_REGEX = r"^[bB](ase)?[0-9]*$"
VERSION_REGEX = r"^[vV][0-9]*$"

NOTE_LEN = (4)
BAR_LEN = (NOTE_LEN*4)
PHRASE_LEN = (BAR_LEN*4)

EMPTY_BAR = " " * BAR_LEN
DIRECTOR_INTRO = "1   2   3   y   "


class Performance:

  @staticmethod
  def create(cfg, raw_sections):
    _sec = copy.deepcopy(raw_sections)
    Performance._pad_all_sections(_sec)

    _intro = _sec[INTRO_KEY] if INTRO_KEY in _sec else None
    _end = _sec[END_KEY] if END_KEY in _sec else None

    _bases = {k:v for (k,v) in _sec.items() if re.match(BASE_REGEX, k)}
    _versions = {k:v for (k,v) in _sec.items() if re.match(VERSION_REGEX, k)}

    # Return original sections if no arrangement can be made
    if not _intro or not _end or not _bases:
      return raw_sections

    new_sections = {}
    new_sections[INTRO_KEY] = Performance._prepare_intro(cfg, _intro)

    for (base_name, base) in _bases.items():
      new_base = Performance._prepare_base(cfg, base)
      new_sections[base_name] = new_base

      for (version_name, version) in _versions.items():
        new_version_name = f"{base_name}{version_name}"
        new_version = Performance._prepare_version(cfg, new_base, version)
        new_sections[new_version_name] = new_version

    new_sections[END_KEY] = Performance._prepare_end(cfg, _end)

    return new_sections


  @staticmethod
  def _pad_all_sections(raw_sections):
    for section in raw_sections.values():
      max_len = 0

      for (instrument, track) in section.items():
        if len(track) > max_len:
          max_len = len(track)

      if max_len % BAR_LEN:
        max_len = BAR_LEN * math.ceil(max_len/BAR_LEN)

      for (instrument, track) in section.items():
        section[instrument] = Performance._pad_track(track, max_len)


  @staticmethod
  def _pad_track(track, max_len, pad_right=True):
    if len(track) < max_len:
      if pad_right:
        return track + (" " * (max_len - len(track)))
      else:
        return (" " * (max_len - len(track))) + track
    else:
      return track


  @staticmethod
  def _prepare_intro(cfg, section):
    num_n16 = len(section[list(section.keys())[0]])
    num_bars = num_n16 / BAR_LEN

    retval = {k:Performance._pad_track(v, PHRASE_LEN, False) for (k,v) in section.items()}

    # Director's track (ONLY if not empty)
    if not retval[cfg.Simulator.director_instrument].strip():
      if num_bars == 1:
        retval[cfg.Simulator.director_instrument] = f"{EMPTY_BAR}{EMPTY_BAR}{DIRECTOR_INTRO}{EMPTY_BAR}"
      elif num_bars == 2:
        retval[cfg.Simulator.director_instrument] = f"{EMPTY_BAR}{DIRECTOR_INTRO}{EMPTY_BAR}{EMPTY_BAR}"
      elif num_bars == 3:
        retval[cfg.Simulator.director_instrument] = f"{DIRECTOR_INTRO}{EMPTY_BAR}{EMPTY_BAR}{EMPTY_BAR}"
      else:
        retval[cfg.Simulator.director_instrument] = f"{EMPTY_BAR}{EMPTY_BAR}{EMPTY_BAR}{DIRECTOR_INTRO}"

    return retval


  @staticmethod
  def _prepare_end(cfg, section):
    retval = {k:Performance._pad_track(v, PHRASE_LEN) for (k,v) in section.items()}
    return retval


  @staticmethod
  def _prepare_base(cfg, section):
    num_n16 = len(section[list(section.keys())[0]])
    num_bars = num_n16 / BAR_LEN

    retval = {}
    for (instrument, track) in section.items():
      if num_bars == 1:
        retval[instrument] = track * 4
      elif num_bars == 2:
        retval[instrument] = track * 2
      elif num_bars == 3:
        retval[instrument] = track + EMPTY_BAR
      else:
        retval[instrument] = track

    return retval


  @staticmethod
  def _prepare_version(cfg, base, version):
    num_n16 = len(version[list(version.keys())[0]])
    num_bars = num_n16 / BAR_LEN

    retval = {}

    for (instrument, track) in version.items():
      if num_bars == 1:
        retval[instrument] = base[instrument][:BAR_LEN*3] + track
      elif num_bars == 2:
        retval[instrument] = base[instrument][:BAR_LEN*2] + track
      elif num_bars == 3:
        retval[instrument] = base[instrument][:BAR_LEN] + track
      else:
        retval[instrument] = track

    # Director's track
    if num_bars == 1:
      retval[cfg.Simulator.director_instrument] = f"{EMPTY_BAR}{EMPTY_BAR}{DIRECTOR_INTRO}{EMPTY_BAR}"
    elif num_bars == 2:
      retval[cfg.Simulator.director_instrument] = f"{EMPTY_BAR}{DIRECTOR_INTRO}{EMPTY_BAR}{EMPTY_BAR}"
    elif num_bars == 3:
      retval[cfg.Simulator.director_instrument] = f"{DIRECTOR_INTRO}{EMPTY_BAR}{EMPTY_BAR}{EMPTY_BAR}"
    else:
      retval[cfg.Simulator.director_instrument] = EMPTY_BAR * 4

    return retval
