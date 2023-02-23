import math
import pygame

from src.textprint import TextPrint

class Display:

  def __init__(self, sim):
    self.sim = sim
    self.cfg = sim.cfg

    _size = [self.cfg.Display.width, self.cfg.Display.height]
    self.screen = pygame.display.set_mode(_size)
    self.header_txt = TextPrint(self.screen, self.cfg, self.cfg.Display.HeaderText)
    self.score_txt = TextPrint(self.screen, self.cfg, self.cfg.Display.ScoreText)
    self.margin = self.cfg.Display.ScoreText.line_height / 2
    pygame.display.set_caption(f"Btu-K simulator")

    self.help_active = False


  def clear(self):
    self.screen.fill(self.cfg.Display.background_color)
    self.header_txt.reset()
    self.score_txt.reset()


  def toggle_help(self):
    self.help_active = not self.help_active


  def update(self):
    self.clear()
    if self.help_active:
      self.show_help()
    else:
      self.show_sim_UI()
    pygame.display.flip()


  def show_help(self):
    self.header_txt.set_color(self.cfg.Display.HeaderText.Color.highlight)
    self.header_txt.indent(self.margin)
    self.header_txt.jump(self.margin)

    txt = f"{self.cfg.App.name} v{self.cfg.App.version} [h:ayuda] "
    self.header_txt.print(txt, color=self.cfg.Display.HeaderText.Color.title)

    self.header_txt.indent(self.margin * 10)
    self.header_txt.print("")
    self.header_txt.print("| Modo normal                          |    | Modo 'jam'                                           |")
    self.header_txt.print("|----------------|---------------------|    |------------------|-----------------------------------|")
    self.header_txt.print("| Tecla          | Función             |    | Tecla            | Función                           |")
    self.header_txt.print("|----------------|---------------------|    |------------------|-----------------------------------|")
    self.header_txt.print("| ESC / q        | salir               |    | 1...0            | ir a sección                      |")
    self.header_txt.print("| ? / h          | mostrar ayuda       |    | SHIFT+1...0      | ir a sección (+10)                |")
    self.header_txt.print("| SPACE          | play/pause          |    | CTRL+1...0       | ir a sección (compás)             |")
    self.header_txt.print("| UP             | anterior sección    |    | CTRL+SHIFT+1...0 | ir a sección (compás) (+10)       |")
    self.header_txt.print("| DOWN           | siguiente sección   |    | BACKSPACE        | Eliminar última sección preparada |")
    self.header_txt.print("| PAGE_UP        | anterior partitura  |                                                            ")
    self.header_txt.print("| PAGE_DOWN      | siguiente partitura |    NOTAS sobre el modo 'jam':                              ")
    self.header_txt.print("| 1...0          | ir a sección        |                                                            ")
    self.header_txt.print("| SHIFT+1...0    | ir a sección (+10)  |    * En modo 'jam', al hacer un cambio de sección, en vez  ")
    self.header_txt.print("| F1...F12       | mute de una pista   |     de hacer el cambio directamente se espera al final     ")
    self.header_txt.print("| SHIFT+F1...F12 | solo de una pista   |     de la sección para hacer el cambio automáticamente.    ")
    self.header_txt.print("| m              | mute (TODAS)        |                                                            ")
    self.header_txt.print("| +              | más BPM             |    * Usando la tecla CTRL se hace que la sección entre al  ")
    self.header_txt.print("| -              | menos BPM           |     próximo cambio de compás.                              ")
    self.header_txt.print("| j              | modo _jam_          |                                                            ")
    self.header_txt.print("| t              | metrónomo           |    * Se pueden acumular secciones programadas y hacer una  ")
    self.header_txt.print("| w              | actualizar part.    |    canción pulsando una secuencia de teclas.               ")
    self.header_txt.print("| SHIFT++        | más BPM (*2)        |")
    self.header_txt.print("| SHIFT+-        | menos BPM (*2)      |")
    self.header_txt.print("| ALT++          | más BPM (+1)        |")
    self.header_txt.print("| ALT+-          | menos BPM (-1)      |")
    self.header_txt.print("| i              | invertir pistas     |")
    self.header_txt.print("| r              | reset sección       |")
    self.header_txt.print("| R              | reset TODAS         |")
    self.header_txt.print("| LEFT           | 1 1/4 izquierda     |")
    self.header_txt.print("| RIGHT          | 1 1/4 derecha       |")
    self.header_txt.print("| SHIFT+LEFT     | 1 1/16 izquierda    |")
    self.header_txt.print("| SHIFT+RIGHT    | 1 1/16 derecha      |")
    self.header_txt.print("| HOME           | inicio de sección   |")
    self.header_txt.print("| END            | fin de sección      |")


  def show_sim_UI(self):
    self.header_txt.indent(self.margin)
    self.score_txt.indent(self.margin)
    self.header_txt.jump(self.margin)
    self.show_header()
    self.header_txt.jump(self.margin)

    self.score_txt.y = self.header_txt.y

    self.show_metronome_line()
    self.score_txt.print()

    track_list = self.sim.score.tracks.keys()
    if self.sim.inverted_tracks:
      track_list = reversed(track_list)

    for (track_index, instrument) in enumerate(track_list):
      track = self.sim.score.tracks[instrument]
      self.show_track_line(track, f"F{track_index+1:<2}({instrument:2}) ")

    self.score_txt.print()
    self.show_jam_timeline(self.sim.jam_pos)


  def show_header(self):
    if self.sim.jam_mode:
      _pos = self.sim.jam_pos
    else:
      _pos = self.sim.score.pos

    _n16 = (_pos % 4) + 1
    _n4 = (math.floor(_pos / 4)) + 1
    _bar = (math.floor(_pos / 4 / 4) + 1) % 4
    _bar = (_bar % 4) if (_bar % 4) else 4
    _phrase = (math.floor(_pos / 4 / 4 / 4) + 1)
    _n4 = (_n4 % 4) if (_n4 % 4) else 4

    _warning_str = ""

    if self.cfg.AutoUpdate.update_available():
      _warning_str += "[ ACTUALIZACION DISPONIBLE! PULSA w ] "

    txt = f"{self.cfg.App.name} v{self.cfg.App.version} [h:ayuda] {_warning_str} "
    _txt_after_active = ""
    _txt_before_active = ""
    _txt_before_scores = txt
    for score in self.cfg.Simulator.scores.values():
      if score == self.sim.score:
        _txt_before_active = txt
        txt += f"[{score.name}] "
        _txt_after_active = txt
      else:
        txt += f"{score.name} "

    self.header_txt.print(txt, newLine=False)
    self.header_txt.print(_txt_after_active, newLine=False, color=self.cfg.Display.HeaderText.Color.highlight)
    self.header_txt.print(_txt_before_active, newLine=False)
    self.header_txt.print(_txt_before_scores, color=self.cfg.Display.HeaderText.Color.title)

    txt = f"[{self.sim.score.name}] secciones: "
    _txt_after_active = ""
    _txt_before_active = ""
    for (index, section) in enumerate(self.sim.score.sections.values()):
      _section_len = int(section.len // (4*4))
      if section == self.sim.score.section:
        _txt_before_active = txt
        txt += f"[{index+1}:{section.name}({_section_len})] "
        _txt_after_active = txt
      else:
        txt += f"{index+1}:{section.name}({_section_len}) "

    self.header_txt.print(txt, newLine=False)
    self.header_txt.print(_txt_after_active, newLine=False, color=self.cfg.Display.HeaderText.Color.highlight)
    self.header_txt.print(_txt_before_active)

    _mute_str = "[MUTE]" if self.sim.muted else ''
    _metronome_str = "[METRÓNOMO]" if self.sim.metronome_active else ''

    _jam_str = ""
    if self.sim.jam_mode:
      _jam_str = f"[JAM {self.format_time(self.sim.jam_time)}]"

    _prep_str = ""
    if self.sim.prepared_section is not None:
      _section_name = self.sim.score.get_section(self.sim.prepared_section).name
      _section_remaining = self.sim.prepared_block_size - (self.sim.score.pos % self.sim.prepared_block_size)
      _remaining_str = f"{int(_section_remaining // 4)}.{_section_remaining % 4}"
      _prep_str = f"[SIGUIENTE en {_remaining_str} -> {self.sim.prepared_section+1}:{_section_name}"
      if self.sim.prepared_sections:
        _prep_str += " ->"
        for (_section_index, _) in self.sim.prepared_sections:
          _section_name = self.sim.score.get_section(_section_index).name
          _prep_str += f"{_section_index+1}->"
        _prep_str = _prep_str[:-2]
      _prep_str += "]"


    txt = f"{self.sim.bpm} bpm" + \
          f" - Pos: {_phrase}.{_bar}.{_n4}.{_n16}" + \
          f" {_mute_str} {_metronome_str} {_jam_str} {_prep_str}"

    self.header_txt.print(txt)
    self.header_txt.print("─"*200)


  def show_metronome_line(self):
    line_prefix = "        "
    _notes = self.cfg.Display.Metronome.text * (math.floor(self.sim.score.section.len / len(self.cfg.Display.Metronome.text)))
    self.score_txt.print(f"{line_prefix} {_notes}", newLine=False)
    self.score_txt.print(f"{line_prefix} {_notes[:self.sim.score.pos+1]}", newLine=False, color=self.cfg.Display.ScoreText.Color.current)
    self.score_txt.print(f"{line_prefix} {_notes[:self.sim.score.pos]}", newLine=False, color=self.cfg.Display.ScoreText.Color.done)
    self.score_txt.print(f"{line_prefix}")


  def show_track_line(self, track, line_prefix):
    if track.muted:
      self.score_txt.print(f"{line_prefix} {track.notes}", color=self.cfg.Display.ScoreText.Color.inactive)
    else:
      self.score_txt.print(f"{line_prefix} {track.notes}", newLine=False)
      self.score_txt.print(f"{line_prefix} {track.notes[:self.sim.score.pos+1]}", newLine=False, color=self.cfg.Display.ScoreText.Color.current)
      self.score_txt.print(f"{line_prefix} {track.notes[:self.sim.score.pos]}", newLine=False, color=self.cfg.Display.ScoreText.Color.done)
      self.score_txt.print(f"{line_prefix}")


  def show_jam_timeline(self, jam_pos):
    _n16 = (jam_pos % 4) + 1
    _n4 = (math.floor(jam_pos / 4)) + 1
    _bar = (math.floor(jam_pos / 4 / 4) + 1) % 4
    _bar = (_bar % 4) if (_bar % 4) else 4
    _phrase = (math.floor(jam_pos / 4 / 4 / 4) + 1)
    _n4 = (_n4 % 4) if (_n4 % 4) else 4

    _n16_per_line = 4*4*4
    _total_lines = 4

    cfg16 = self.cfg.Display.Timeline.N16
    cfg4 = self.cfg.Display.Timeline.N4
    cfgF4 = self.cfg.Display.Timeline.FirstN4

    # Calculate base x/y
    _total_width = (cfg16.width+cfg16.margin_x) * (_n16_per_line)
    _base_x = (self.cfg.Display.width - _total_width) / 2
    _base_y = self.cfg.Display.height - self.margin - ((cfg16.height+cfg16.margin_y)*4)

    # Calculate part of jam to show
    _draw_start_pos = jam_pos - (jam_pos % (_n16_per_line * _total_lines))
    _draw_count = jam_pos - _draw_start_pos

    # Show "ghost" pattern for 4 full bars (if necessary)
    if _draw_count < _n16_per_line:
      for pos in range(_n16_per_line):
        _x = _base_x + (cfg16.width+cfg16.margin_x) * pos
        _y = _base_y

        _color = pygame.Color(0)
        _hsva = list(self.cfg.Display.Timeline.gradient[pos % len(self.cfg.Display.Timeline.gradient)])
        _hsva[2] *= 0.2  # 20% value
        _color.hsva = _hsva
        rect = pygame.Rect(_x, _y, cfg16.width, cfg16.height)
        pygame.draw.rect(self.screen, _color, rect)

    # Show played bars
    for i in range(_draw_count):
      pos = _draw_start_pos + i
      _numline = i // _n16_per_line
      _x = _base_x + (cfg16.width+cfg16.margin_x) * (pos % _n16_per_line)
      _y = _base_y + (cfg16.height+cfg16.margin_y) * math.floor(_numline)
      _color = pygame.Color(0)
      _hsva = list(self.cfg.Display.Timeline.gradient[pos % len(self.cfg.Display.Timeline.gradient)])
      if _numline % 2:
        _hsva[2] *= 0.65  # 65% value
      _color.hsva = _hsva
      rect = pygame.Rect(_x, _y, cfg16.width, cfg16.height)
      pygame.draw.rect(self.screen, _color, rect)

      if not (pos % (4)):
        _int_x = _x + ((cfg16.width-cfg4.width)/2)
        _int_y = _y + ((cfg16.height-cfg4.height)/2)
        rect = pygame.Rect(_int_x, _int_y, cfg4.width, cfg4.height)
        pygame.draw.rect(self.screen, cfg4.color, rect)

      if not (pos % (4*4)):
        _int_x = _x + ((cfg16.width-cfgF4.width)/2)
        _int_y = _y + ((cfg16.height-cfgF4.height)/2)
        rect = pygame.Rect(_int_x, _int_y, cfgF4.width, cfgF4.height)
        pygame.draw.rect(self.screen, cfgF4.color, rect)


  def format_time(self, value):
    milliseconds = value*1000
    hours = milliseconds // (60 * 60 * 1000)
    milliseconds %= (60 * 60 * 1000)
    minutes = milliseconds // (60 * 1000)
    milliseconds %= (60 * 1000)
    seconds = milliseconds // 1000
    milliseconds %= 1000

    return f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds//10):02}"

