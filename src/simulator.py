import pygame

from src.display import Display

ALL_FKEYS = [
  pygame.K_F1,pygame.K_F2,pygame.K_F3,pygame.K_F4,pygame.K_F5,pygame.K_F6,
  pygame.K_F7,pygame.K_F8,pygame.K_F9,pygame.K_F10,pygame.K_F11,pygame.K_F12 ]

ALL_NUMKEYS = [
  pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,
  pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0 ]

ALL_KPNUMKEYS = [
  pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6,
  pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_KP0 ]

class Simulator:

  def __init__(self, cfg):
    print("- Inicializando simulador")

    print("- Inicializando pygame")
    pygame.init()
    pygame.mixer.pre_init(buffer=10240)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)

    cfg.init()

    self.cfg = cfg
    self.cfg_sim = self.cfg.Simulator
    self.running = False
    self.inverted_tracks = False
    self.jam_mode = False
    self.jam_time = 0
    self.bpm = self.cfg_sim.bpm
    self.score_index = 0
    self.jam_pos = 0
    self.prepared_section = None
    self.prepared_sections = []
    self.prepared_block_size = None
    self.display = Display(self)
    self.clock = pygame.time.Clock()

    self.playing = False
    self.muted = False
    self.metronome_active = False
    self.need_update_restart = False


  @property
  def score(self):
    name = list(self.cfg_sim.scores.keys())[self.score_index]
    return self.cfg_sim.scores[name]


  def select_score(self, index):
    if -1 < index < len(self.cfg_sim.scores):
      self.score_index = index
      self.score.reset_section()
      self.score.reset_pos()
      self.prepared_sections = []
      self.prepared_section = None
      self.prepared_block_size = None


  def prev_score(self):
    self.score_index -= 1
    if self.score_index < 0:
      self.score_index = len(self.cfg_sim.scores)-1
    self.score.reset_section()
    self.score.reset_pos()
    if not self.jam_mode:
      self.jam_pos = 0
    self.prepared_sections = []
    self.prepared_section = None
    self.prepared_block_size = None


  def next_score(self):
    self.score_index = (self.score_index + 1) % len(self.cfg_sim.scores)
    self.score.reset_section()
    self.score.reset_pos()
    if not self.jam_mode:
      self.jam_pos = 0
    self.prepared_sections = []
    self.prepared_section = None
    self.prepared_block_size = None


  def prev_section(self):
    self.score.prev_section()
    if not self.jam_mode:
      self.jam_pos = 0


  def next_section(self):
    self.score.next_section()
    if not self.jam_mode:
      self.jam_pos = 0


  def prepare_section(self, section_index, block_size=None):
    if section_index < 0 or section_index >= len(self.score.sections):
      return

    if block_size is None:
      if self.prepared_sections:
        (_last_section_index, _) = self.prepared_sections[-1]
        _last_section = self.score.get_section(_last_section_index)
        _block_size = _last_section.len
      else:
        _block_size = self.score.section.len
    else:
      _block_size = block_size

    if self.prepared_section is None:
      self.prepared_section = section_index
      self.prepared_block_size = _block_size
    else:
      self.prepared_sections.append( (section_index, _block_size) )


  def reset_all(self):
    self.jam_pos = 0
    self.jam_time = 0
    for score in self.cfg_sim.scores.values():
      score.reset_all_sections()


  def reset_score(self):
    self.jam_pos = 0
    self.jam_time = 0
    self.score.reset_all_sections()


  def reset_section(self):
    self.jam_pos = 0
    self.jam_time = 0
    self.score.reset()


  def apply_resource_updates(self):
    if not self.cfg.AutoUpdate.update_available():
      print("- No hay actualizaciones disponibles")
      return

    if self.cfg.apply_resource_updates():
      self.need_update_restart = True


  def close(self):
    # No restarting until it works... :)
    self.need_update_restart = False
    self.running = False



  def check_user_events(self):
    for event in pygame.event.get():

      if event.type == pygame.QUIT: self.close()

      elif event.type == pygame.KEYDOWN:
        _mods = pygame.key.get_mods()

        if event.key == pygame.K_ESCAPE:      self.close()
        elif event.key == pygame.K_q:         self.close()

        elif event.key == pygame.K_h:         self.display.toggle_help()

        elif event.key == pygame.K_HOME:      self.score.go_to_start()
        elif event.key == pygame.K_END:       self.score.go_to_end()

        elif event.key == pygame.K_SPACE:     self.playing = not self.playing
        elif event.key == pygame.K_m:         self.muted = not self.muted

        elif event.key == pygame.K_t:         self.metronome_active = not self.metronome_active

        elif event.key == pygame.K_i:         self.inverted_tracks = not self.inverted_tracks

        elif event.key == pygame.K_j:
          self.jam_mode = not self.jam_mode
          self.jam_pos = 0
          self.jam_time = 0
          self.prepared_sections = []
          self.prepared_section = None
          self.prepared_block_size = None
          self.reset_section()

        if self.jam_mode:
          if event.key == pygame.K_BACKSPACE:
            if self.prepared_sections:
              self.prepared_sections.pop()
            elif self.prepare_section is not None:
              self.prepared_section = None
              self.prepared_block_size = None


        if not (_mods & (pygame.KMOD_SHIFT | pygame.KMOD_CTRL | pygame.KMOD_ALT )):
          #
          # NO MODIFIERS
          #

          if event.key == pygame.K_LEFT:
            self.score.shift_n4(-1)
          elif event.key == pygame.K_RIGHT:
            self.score.shift_n4(+1)

          elif event.key == pygame.K_r: self.reset_section()

          elif event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:  self.bpm += self.cfg_sim.bpm_increment
          elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]: self.bpm -= self.cfg_sim.bpm_increment

          elif event.key == pygame.K_PAGEUP:   self.prev_score()
          elif event.key == pygame.K_PAGEDOWN: self.next_score()

          elif event.key == pygame.K_UP:   self.prev_section()
          elif event.key == pygame.K_DOWN: self.next_section()

          elif event.key == pygame.K_w: self.apply_resource_updates()

          if self.jam_mode:
            [self.prepare_section(i) for (i,k) in enumerate(ALL_NUMKEYS) if k == event.key]
            [self.prepare_section(i) for (i,k) in enumerate(ALL_KPNUMKEYS) if k == event.key]
          else:
            [self.score.select_section(i) for (i,k) in enumerate(ALL_NUMKEYS) if k == event.key]
            [self.score.select_section(i) for (i,k) in enumerate(ALL_KPNUMKEYS) if k == event.key]

          if self.inverted_tracks:
            [self.score.toggle_track_mute(self.score.section.num_tracks -i -1) for (i,k) in enumerate(ALL_FKEYS) if k == event.key]
          else:
            [self.score.toggle_track_mute(i) for (i,k) in enumerate(ALL_FKEYS) if k == event.key]

        elif _mods & pygame.KMOD_SHIFT and not (_mods & (pygame.KMOD_CTRL | pygame.KMOD_ALT )):
          #
          # <SHIFT> pressed
          #

          if event.key == pygame.K_LEFT:
            self.score.shift_n16(-1)
          elif event.key == pygame.K_RIGHT:
            self.score.shift_n16(+1)

          elif event.key == pygame.K_r: self.reset_all()

          elif event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:  self.bpm += self.cfg_sim.bpm_increment * 2
          elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]: self.bpm -= self.cfg_sim.bpm_increment * 2

          if self.jam_mode:
            [self.prepare_section(i+10) for (i,k) in enumerate(ALL_NUMKEYS) if k == event.key]
            [self.prepare_section(i+10) for (i,k) in enumerate(ALL_KPNUMKEYS) if k == event.key]
          else:
            [self.score.select_section(i+10) for (i,k) in enumerate(ALL_NUMKEYS) if k == event.key]
            [self.score.select_section(i+10) for (i,k) in enumerate(ALL_KPNUMKEYS) if k == event.key]

          if self.inverted_tracks:
            [self.score.toggle_track_solo(self.score.section.num_tracks -i -1) for (i,k) in enumerate(ALL_FKEYS) if k == event.key]
          else:
            [self.score.toggle_track_solo(i) for (i,k) in enumerate(ALL_FKEYS) if k == event.key]

        elif _mods & pygame.KMOD_ALT and not (_mods & (pygame.KMOD_SHIFT | pygame.KMOD_CTRL )):
          #
          # <ALT> pressed
          #

          if   event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:  self.bpm += 1
          elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]: self.bpm -= 1

        elif _mods & pygame.KMOD_CTRL and not (_mods & (pygame.KMOD_SHIFT | pygame.KMOD_ALT )):
          #
          # <CTRL> pressed
          #

          if self.jam_mode:
            [self.prepare_section(i, 4*4) for (i,k) in enumerate(ALL_NUMKEYS) if k == event.key]
            [self.prepare_section(i, 4*4) for (i,k) in enumerate(ALL_KPNUMKEYS) if k == event.key]

        elif _mods & pygame.KMOD_CTRL and _mods & pygame.KMOD_SHIFT and not (_mods & (pygame.KMOD_ALT )):
          #
          # <CTRL+SHIFT> pressed
          #

          if self.jam_mode:
            [self.prepare_section(i+10, 4*4) for (i,k) in enumerate(ALL_NUMKEYS) if k == event.key]
            [self.prepare_section(i+10, 4*4) for (i,k) in enumerate(ALL_KPNUMKEYS) if k == event.key]

      if not self.running:
        return


  def run(self):
    print("- Arrancando simulador")
    self.running = True

    while self.running:

      self.check_user_events()
      self.display.update()

      if self.playing:

        if self.metronome_active:
          self.cfg_sim.metronome_track.play(self.score.pos)

        if not self.muted:
          for track in self.score.tracks.values():
            track.play(self.score.pos)

        self.score.shift_n16(+1)
        if self.jam_mode:
          self.jam_pos += 1
          self.jam_time += 60 / (self.bpm*4)

      if self.jam_mode:
        if self.prepared_section is not None:
          if self.score.pos % self.prepared_block_size == 0:  # selection end!
            self.score.select_section(self.prepared_section)
            if self.prepared_sections:
              (self.prepared_section, self.prepared_block_size) = self.prepared_sections.pop(0)
            else:
              self.prepared_section = None
              self.prepared_block_size = None
      else:
        self.jam_pos = self.score.pos

      fps = (self.bpm/60)*4
      self.clock.tick(fps)

    print("- Cerrando simulador")
    pygame.quit()

