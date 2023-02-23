import math
import pygame

from src.track import Track

class Section:

  def __init__(self, cfg, name, tracks):
    self.cfg = cfg
    self.name = name
    self.tracks = {k:Track(cfg,k,v) for (k,v) in tracks.items()}
    self.num_tracks = len(self.tracks)
    self.normalize_track_length()
    self.len = self.get_track(0).len
    self.pos = 0

    ch_num = 1
    for (instrument, track) in self.tracks.items():
      if instrument in self.cfg.Simulator.instruments:
        track.channel = pygame.mixer.Channel(ch_num)
        ch_num += 1
      else:
        track.valid = False


  def normalize_track_length(self):
    max_len = 0
    for track in self.tracks.values():
      if track.len > max_len:
        max_len = track.len

    # Bar padding
    _bar_len = (4*4)
    if max_len % _bar_len:
      max_len = _bar_len * math.ceil(max_len/_bar_len)

    for track in self.tracks.values():
      if track.len < max_len:
        track.pad_notes(max_len)


  def get_track(self, index):
    if index < 0 or index >= len(self.tracks):
      return None

    instrument = list(self.tracks.keys())[index]
    return self.tracks[instrument]


  def reset_pos(self):
    self.pos = 0


  def go_to_start(self):
    self.reset_pos()


  def go_to_end(self):
    self.pos = self.len-1


  def reset(self):
    self.reset_pos()
    for track in self.tracks.values():
      track.unmute()


  def shift_n16(self, n16=1):
    self.pos = (self.pos + n16) % self.len


  def shift_n4(self, n4=1):
    offset = self.pos % 4
    if not offset:
      self.shift_n16(n4*4)
    else:
      if n4 > 0:
        self.shift_n16(4-offset)
      else:
        self.shift_n16(offset*-1)


  def toggle_track_mute(self, index):
    track = self.get_track(index)
    if not track:
      return

    track.toggle_mute()


  def toggle_track_solo(self, index):
    track = self.get_track(index)
    if not track:
      return

    other_muted = [t.muted for t in self.tracks.values() if t is not track]

    if track.muted:
      track.unmute()
      [t.mute() for t in self.tracks.values() if t is not track]
    else:
      if all(other_muted):
        [t.unmute() for t in self.tracks.values() if t is not track]
      else:
        [t.mute() for t in self.tracks.values() if t is not track]

