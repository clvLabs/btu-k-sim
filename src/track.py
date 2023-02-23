
class Track:

  def __init__(self, cfg, instrument, notes):
    self.cfg = cfg
    self.instrument = self.cfg.Simulator.instruments[instrument]
    self.notes = self._parse_notes(notes)
    self.len = len(self.notes)
    self.valid = True
    self.muted = False
    self.channel = None


  def play(self, pos):
    if not self.valid or self.muted:
      return

    sample = self.get_sample(pos)

    if not sample:
      return

    try:
      self.channel.play(sample)
    except Exception as e:
      pass


  def _parse_notes(self, notes):
    expanded = ""
    repeated_section = ""
    for note in notes:
      if note == "=":
        if expanded == "":
          expanded = repeated_section * 2
        else:
          expanded += repeated_section
      else:
        if expanded == "":
          repeated_section += note
        else:
          expanded += note

    if expanded == "":
      expanded = repeated_section

    return expanded


  def pad_notes(self, max_len):
    padding = max_len - self.len
    self.len = max_len
    self.notes += " " * padding


  def get_sample(self, pos):
    if not self.valid or self.muted:
      return None

    if pos < 0 or pos >= len(self.notes):
      return None

    curr_note = self.notes[pos]
    if curr_note in self.instrument.samples:
      return self.instrument.samples[curr_note]

    return None


  def toggle_mute(self):
    if self.valid:
      self.muted = not self.muted


  def set_mute(self, muted=True):
    if self.valid:
      self.muted = muted


  def mute(self):
    self.set_mute(True)


  def unmute(self):
    self.set_mute(False)
